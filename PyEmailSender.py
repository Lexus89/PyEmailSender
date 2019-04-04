import argparse
import glob

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


def send_message(args):
    if args is None:
        return False

    smtp_host = args["host"]
    smtp_port = int(args["port"])
    smtp_ssl = bool(args["ssl"])
    username = args["username"]
    password = args["password"]
    recipients_file = args["recipients_file"]
    from_name = args["from_name"]
    from_email = args["from_email"]
    from_full = '{} <{}>'.format(from_name, from_email)
    subject = args["subject"]
    message_file = args["message_file"]
    message_type = args["message_type"]
    attachments_dir = args["attachments_dir"]

    if not os.path.isfile(message_file):
        return False

    message_body = read_file(message_file)

    if not os.path.isfile(recipients_file):
        return False

    recipients = read_file_lines(recipients_file)

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = from_full
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments_path_list = None
    if os.path.isdir(attachments_dir):
        attachments_path_list = get_file_set_in_dir(attachments_dir, True)

    if attachments_path_list is not None:
        for file in attachments_path_list:
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

    if message_type == 'html':
        outer.attach(MIMEText(message_body, 'html'))
    else:
        outer.attach(MIMEText(message_body, 'plain'))

    composed = outer.as_string()

    # send email
    try:
        with smtplib.SMTP('{}: {}'.format(smtp_host, smtp_port)) as server:
            server.ehlo()
            if smtp_ssl:
                server.starttls()
                server.ehlo()

            server.login(username, password)
            server.sendmail(from_full, recipients, composed)

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


def get_file_set_in_dir(dir_path, files_only, filters=None):
    """
    Scan for files in a given directory path
    :param dir_path: directory path
    :param files_only: If set to False then will get files and directories list. True will get only files list in given directory path
    :param filters: file extensions: example ['*', '*.*', '*.txt']
    :return: Set of files that matches given filters
    """
    file_path_set = set()
    if filters is None:
        filters = ['*']

    for f in filters:
        for path in glob.glob(os.path.join(dir_path, f)):
            if files_only:
                if os.path.isfile(path):
                    file_path_set.add(path)
            else:
                file_path_set.add(path)
    return file_path_set


def run(args):
    try:
        if not send_message(args):
            print('[-] Could not send the message.')
            arg_parser.print_help()
    except Exception as e:
        print('[-] ERROR: {}'.format(e))
        arg_parser.print_help()

    sys.exit(0)


def generate_argparser():
    ap = argparse.ArgumentParser()

    ap.add_argument("-l", "--host", action='store',
                    help="SMTP host IP/Domain")

    ap.add_argument("-p", "--port", action='store', type=int, default=587,
                    help="SMTP server port")

    ap.add_argument("-s", "--ssl", action='store_true',
                    help="SMTP server require SSL/TLS")

    ap.add_argument("-u", "--username", action='store',
                    help="SMTP account username")

    ap.add_argument("-w", "--password", action='store',
                    help="SMTP account password")

    ap.add_argument("-e", "--from-email", action='store',
                    help="Sender email")

    ap.add_argument("-n", "--from-name", action='store',
                    help="Sender name")

    ap.add_argument("-r", "--recipients-file", action='store',
                    help="Path to recipient(s) email(s) file. New line separated")

    ap.add_argument("-b", "--subject", action='store',
                    help="Message subject")

    ap.add_argument("-m", "--message-file", action='store',
                    help="Path to file containing the message")

    ap.add_argument("-t", "--message-type", action='store', choices=['html', 'plain'],
                    help="Message body type")

    ap.add_argument("-i", "--attachments-dir", action='store',
                    help="Path to a attachments directory. Files within specified path will be attached to the message.")


    return ap


def main():
    global arg_parser
    arg_parser = generate_argparser()
    args = vars(arg_parser.parse_args())
    run(args)


if __name__ == "__main__":
    main()
