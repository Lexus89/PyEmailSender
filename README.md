Python mass email sender with multiple attachments support

### Usage

```
usage: test.py [-h] [-l HOST] [-p PORT] [-s] [-u USERNAME] [-w PASSWORD]
               [-e FROM_EMAIL] [-n FROM_NAME] [-r RECIPIENTS_FILE]
               [-b SUBJECT] [-m MESSAGE_FILE] [-t {html,plain}]
               [-i ATTACHMENTS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -l HOST, --host HOST  SMTP host IP/Domain
  -p PORT, --port PORT  SMTP server port
  -s, --ssl             SMTP server require SSL/TLS
  -u USERNAME, --username USERNAME
                        SMTP account username
  -w PASSWORD, --password PASSWORD
                        SMTP account password
  -e FROM_EMAIL, --from-email FROM_EMAIL
                        Sender email
  -n FROM_NAME, --from-name FROM_NAME
                        Sender name
  -r RECIPIENTS_FILE, --recipients-file RECIPIENTS_FILE
                        Path to recipient(s) email(s) file. New line separated
  -b SUBJECT, --subject SUBJECT
                        Message subject
  -m MESSAGE_FILE, --message-file MESSAGE_FILE
                        Path to file containing the message
  -t {html,plain}, --message-type {html,plain}
                        Message body type
  -i ATTACHMENTS_DIR, --attachments-dir ATTACHMENTS_DIR
                        Path to a attachments directory. Files within
                        specified path will be attached to the message.

```
