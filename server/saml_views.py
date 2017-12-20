"""Adds SAML single sign-on (SSO) support to the application.
"""
import flask
import requests
import saml2
import saml2.config
import saml2.client
from server import app
from .utils import get_redirect_target


def load_saml_metadata():
    metadata_url = app.config['SAML_METADATA_URL']
    response = requests.get(metadata_url)
    assert response.status_code == 200
    return response.text


def saml_client():
    metadata = load_saml_metadata()  # TODO cache

    metadata_url = flask.url_for('saml_metadata', _external=True)
    acs_url = flask.url_for('saml_acs', _external=True)

    config = saml2.config.Config()
    config.load({
        'entityid': metadata_url,
        'metadata': {'inline': [metadata]},
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, saml2.BINDING_HTTP_POST),
                    ],
                },
            },
            'allow_unsolicited': True,
            'authn_requests_signed': False,
            'logout_requests_signed': True,
            'want_assertions_signed': True,
            'want_response_signed': False,
        },
        'allow_unknown_attributes': True,
    })
    client = saml2.client.Saml2Client(config=config)
    return client


@app.route('/saml/login')
def login():
    next_url = get_redirect_target()

    client = saml_client()
    reqid, info = client.prepare_for_authenticate(relay_state=next_url)

    headers = dict(info['headers'])
    response = flask.redirect(headers.pop('Location'), code=302)
    response.headers.extend(headers)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/saml/acs', methods=['GET', 'POST'])
def saml_acs():
    if 'SAMLResponse' not in flask.request.form:
        return 'missing SAMLResponse', 500

    app.logger.debug('got SAML response')
    client = saml_client()
    response = client.parse_authn_request_response(
        flask.request.form['SAMLResponse'],
        saml2.entity.BINDING_HTTP_POST,
    )
    print(response)


@app.route('/saml/metadata')
def saml_metadata():
    client = saml_client()

    metadata_str = saml2.metadata.create_metadata_string(
        configfile=None,
        config=client.config,
    )
    return metadata_str, {'Content-Type': 'text/xml'}
