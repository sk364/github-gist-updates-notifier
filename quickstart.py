import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = 'https://mail.google.com/'
APPLICATION_NAME = 'Send PR Conflicts Mail'

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()
except ImportError:
    flags = None

def get_credentials(client_secret_file='client_secret.json', credentials_file='credentials.json'):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = '/home/sachin'
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, credentials_file)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

if __name__ == '__main__':
    get_credentials(credentials_file='credentials_pr.json')
