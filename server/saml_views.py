"""Adds SAML single sign-on (SSO) support to the application.
"""
import flask
from flask import g, flash, redirect
import requests
import saml2
import saml2.config
import saml2.client
from server import app
from flask_login import login_user, logout_user

from .utils import get_redirect_target, is_safe_url, random_string
from .models import Student, Professor


def load_saml_metadata():
    metadata_url = app.config['SAML_METADATA_URL']
    response = requests.get(metadata_url)
    assert response.status_code == 200
    return response.text


def saml_client(metadata):
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

                # Without this, the saml2 library "helpfully" keeps track of
                # the requests we've issued and rejects ones it doesn't know
                # about. The client object is not persistent here, though.
                'allow_unsolicited': True,
            },
        },
    })
    client = saml2.client.Saml2Client(config=config)
    return client


@app.before_request
def set_up_saml_client():
    if not hasattr(g, 'saml_client'):
        # Load the metadata from the endpoint, but only once.
        if 'SAML_METADATA' in app.config:
            metadata = app.config['SAML_METADATA']
        else:
            metadata = load_saml_metadata()
            app.config['SAML_METADATA'] = metadata

        # Create the client object.
        g.saml_client = saml_client(metadata)


@app.route('/login')
def login():
    next_url = get_redirect_target()
    reqid, info = g.saml_client.prepare_for_authenticate(relay_state=next_url)

    headers = dict(info['headers'])
    response = flask.redirect(headers.pop('Location'), code=302)
    response.headers.extend(headers)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/logout')
def logout():
    logout_user()
    return redirect(app.config['BASE_URL'])


@app.route('/saml/acs', methods=['GET', 'POST'])
def saml_acs():
    if 'SAMLResponse' not in flask.request.form:
        return 'missing SAMLResponse', 500

    # Parse the SAML response.
    app.logger.debug('got SAML response')
    response = g.saml_client.parse_authn_request_response(
        flask.request.form['SAMLResponse'],
        saml2.entity.BINDING_HTTP_POST,
    )

    # Get the URL to redirect to when don.
    next_url = flask.request.form.get('RelayState')
    if not next_url or not is_safe_url(next_url):
        next_url = app.config['BASE_URL']

    # Get details about the user.
    identity = response.get_identity()
    uid = identity['uid'][0]
    email = identity['mail'][0]
    app.logger.debug('authenticated %s', email)

    # Try to log in an existing user.
    user = Student.get_student_by_netid(uid) or \
        Professor.get_professor_by_netid(uid)
    if user:
        login_user(user)
        flash('Welcome back, %s!' % user.name)
        return redirect(next_url)

    # Otherwise, register a new user.
    is_faculty = 'faculty' in identity['eduPersonAffiliation']
    name = identity['cn'][0]
    if is_faculty:
        user = Professor.create_professor(
            net_id=uid,
            name=name,
            email=email,
            password=random_string(),
        )
    else:
        user = Student.create_student(
            net_id=uid,
            name=name,
            email=email,
            password=random_string(),
        )
    login_user(user)
    flash('Welcome, %s!' % user.name)
    return redirect(next_url)


@app.route('/saml/metadata')
def saml_metadata():
    metadata_str = saml2.metadata.create_metadata_string(
        configfile=None,
        config=g.saml_client.config,
    )
    return metadata_str, {'Content-Type': 'text/xml'}
