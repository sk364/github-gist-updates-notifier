import base64
import httplib2
from email.mime.text import MIMEText
from apiclient import discovery, errors

from mailer_config import CLIENT_SECRET_FILE, CREDENTIALS_FILE_NAME
from quickstart import get_credentials


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_mail(recipients, subject, body):
    credentials = get_credentials(client_secret_file=CLIENT_SECRET_FILE, credentials_file=CREDENTIALS_FILE_NAME)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    body = 'Gist URLs : {}'.format(body)

    for recipient in recipients:
        raw_message = create_message('me', recipient, subject, body)

        try:
            message = (service.users().messages().send(userId='me', body=raw_message).execute())
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
