import csv
import urllib.request
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os

def check_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        print('Connected!')
        return True
    except:
        print('Offline!')
        return False # test

def main_loop():
    if check_connection():
        send_mail()
    else:
        collect_data()

def send_mail():
    filename = 'data.csv'
    attachment = open(filename, 'rb')
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', 'attachment; filename = ' + filename)

    email_sender = 'oceansentinel.user@gmail.com'
    email_password = 'shrnzgkefspeutnp'
    email_receiver = 'oceansentinel.data@gmail.com'

    subject = 'Data från Python'
    body = 'Daniel har en klitoris under sin pung'

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em.attach(MIMEText(body, 'plain'))
    em.attach(attachment_package)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    os.remove('data.csv')

    print('Email sent!')

def collect_data():
    time.sleep(5)
    while True:
        time.sleep(2)
        with open('data.csv', 'a', newline = '') as file:
            writer = csv.writer(file)
            data = ['12', '28W', '29E', '10:39']
            writer.writerow(data)
