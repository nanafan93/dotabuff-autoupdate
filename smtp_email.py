import os
import smtplib
from email.message import EmailMessage
email = os.environ.get('EMAIL_ADDRESS')
pwd = os.environ.get('GMAIL_PYTHON_APP-PWD')
target = ['shubhankarranade30@gmail.com','shibbugokhale@gmail.com']
msg = EmailMessage()
msg['Subject'] = 'Dotabuff Update'
msg['From'] = email
msg['To'] = target
msg.set_content('Hello dear a test message from python :)')
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email,pwd)
    smtp.send_message(msg)
    