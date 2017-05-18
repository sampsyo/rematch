""" Random functions that didn't quite fit anywhere else. """


def send_email(recipient, subject, content):

    print 'WARNING: Email is currently disabled.  Please configure the ' \
          'SMTPlib appropriately in server/utils.py'
    return

    import smtplib
    from email.mime.text import MIMEText

    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = 'no.reply@example.com'
    message['To'] = recipient

    s = smtplib.SMTP('localhost')
    s.sendmail('no.reply@example.com', [recipient], message.as_string())
    s.quit()
