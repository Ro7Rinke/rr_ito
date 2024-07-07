import smtplib, ssl
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_password_reset_email(to_email, reset_url):
    
    message = MIMEText(f"Click the link to reset your password: {reset_url}")
    message['Subject'] = 'Password Reset'

    send_email(to_email, message)

def send_email(to_email, message):
    smtp_server = os.getenv('SMTP_SERVER')
    port = int(os.getenv('EMAIL_PORT'))
    sender_email = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')

    message['From'] = sender_email
    message['To'] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())
