"""Random functions that didn't quite fit anywhere else."""
from config import FROM_EMAIL


def send_email(recipient, subject, content):

    print 'WARNING: Email is currently disabled.  Please configure the ' \
          'SMTPlib appropriately in server/utils.py'
    return

    import smtplib
    from email.mime.text import MIMEText

    message = MIMEText(content)
    message['Subject'] = subject
    message['From'] = FROM_EMAIL
    message['To'] = recipient

    s = smtplib.SMTP('localhost')
    s.sendmail(FROM_EMAIL, [recipient], message.as_string())
    s.quit()
