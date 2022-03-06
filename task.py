from models import Users
from __init__ import celery
from flask import current_app
from email.message import EmailMessage
import smtplib

@celery.task
def notify_newsletter(url):
    users = Users.query.all()
    for user in users:
        if user.subscribe:
            email_name = current_app.config.get("EMAIL_NAME")
            email_passwd = current_app.config.get("EMAIL_PASSWORD")
            print("email send to {}".format(user.email))
            send_email(email_name, email_passwd, user.email, url)

def send_email(from_email, passwd, to_email, url):

    mail = EmailMessage()
    mail.set_content("new blog at {url}".format(url=url))

    mail["Subject"] = "New blog!"
    mail["From"] = from_email
    mail["To"] = to_email

    user = from_email

    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()

        server_ssl.login(user, passwd)

        server_ssl.send_message(mail, from_email, to_email)
        
        server_ssl.close()
        print("email send!")

    except Exception as e:
        print("nieco sa pokazilo")
        print.error(e)