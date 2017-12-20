"""Random functions that didn't quite fit anywhere else."""
from server import app
from urlparse import urlparse, urljoin
from flask import request


def send_email(recipient, subject, content):

    app.logger.warn('Email is currently disabled.  Please configure the '
                    'SMTPlib appropriately in server/utils.py')
    return

    import smtplib
    from email.mime.text import MIMEText

    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = app.config['FROM_EMAIL']
    message['To'] = recipient

    s = smtplib.SMTP('localhost')
    s.sendmail(app.config['FROM_EMAIL'], [recipient], message.as_string())
    s.quit()


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# http://flask.pocoo.org/snippets/62/
def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
