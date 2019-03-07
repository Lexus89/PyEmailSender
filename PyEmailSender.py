#!/usr/local/bin/python3

"""
Email sender with attachment support
"""

import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import sys

COMMASPACE = ', '


def send_message(dict_msg_attr):
    if dict_msg_attr is None:
        return False

    username = dict_msg_attr["username"]
    password = dict_msg_attr["password"]
    smtp_host = dict_msg_attr["server"]
    smtp_port = int(dict_msg_attr["port"])
    smtp_ssl = bool(dict_msg_attr["ssl"])
    recipients = dict_msg_attr["recipients"]
    #message_plain = dict_msg_attr["message_plain"]
    message_html = dict_msg_attr["message_html"]

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = dict_msg_attr["subject"]
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = dict_msg_attr["from"]
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = dict_msg_attr["attachments"]
    if attachments is not None:
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

    #outer.attach(MIMEText(message_plain, 'plain'))
    outer.attach(MIMEText(message_html, 'html'))
    composed = outer.as_string()

    # send email
    try:
        with smtplib.SMTP('{}: {}'.format(smtp_host, smtp_port)) as server:
            server.ehlo()
            if smtp_ssl:
                server.starttls()
                server.ehlo()

            server.login(username, password)
            server.sendmail(dict_msg_attr["from"], recipients, composed)

            server.close()
            server.close()

            return True

    except:
        print("Sending email failed. More info {}: ".format(sys.exc_info()[0]), sys.exc_info()[0])
        raise


def read_file(file_path):
    with open(file_path) as fp:
        return fp.read()


def read_file_lines(file_path):
    with open(file_path) as fp:
        return fp.readlines()


#message_plain = read_file("/Users/moda/Desktop/Email_Template/message.txt")
message_html = read_file("/home/cod/Email_Template/message.html")
message_subject = "Billing statement for October"
recipients = read_file_lines("/home/cod/Email_Template/recipients.txt")

# multiple attachments are supported
attachments = ["/home/cod/Email_Template/billing.pdf"]

for recipient in recipients:
    dict_msg = {
        "username": "email1@company.local",
        "password": "123456",
        "server": "smtp.gmail.com",
        "port": 587,
        "ssl": True,
        "from": "Company Name <email1@company.local>",
        "recipients": [recipient],
        #"message_plain": message_plain,
        "message_html": message_html,
        "subject": message_subject,
        "attachments": attachments
    }

    isSent = send_message(dict_msg)
    if isSent:
        print("Sent: {}".format(recipient), end='')
