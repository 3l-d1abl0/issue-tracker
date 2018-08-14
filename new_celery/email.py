import smtplib

def send_email(email_address, subject, body=None):
    if not body:
        body = subject
        subject = 'No Subject'

    #user = os.environ['MAIL_ADDRESS']
    user = 'user@email.com'
    #password = os.environ['MAIL_PASSWORD']
    password = 'userEmailPassword'


    sent_from = user
    to = [email_address]

    email_text = """\
    From: %s
    To: %s
    Subject: %s
%s
    """ % (sent_from, ", ".join(to), subject, body)

    #print email_text

    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.ehlo()
    server.login(user, password)
    server.sendmail(sent_from, to, email_text)
    server.close()
