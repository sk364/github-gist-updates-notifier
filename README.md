**Note**: This will only monitor the starred gists.

# Installation

Create a virtualenv -  
> virtualenv notifierenv

Activate the virtualenv -  
> source notifierenv/bin/activate

Install all dependencies in `requirements.txt` using `pip`.  
> pip install -r requirements.txt

Run these commands to create `config.py` and `mailer_config.py` from the default skeletons.
> cp config.py.default config.py  
> cp mailer_config.py.default mailer_config.py

Create a personal access token in your GitHub account. (Settings -> Personal Access Tokens (under Developer Settings tab in left sidebar))  
Copy paste the token in `config.py`.  
Finally, add recipients of the notifying mails of your choice in config.  

Follow [Google API Developer Quickstart](https://developers.google.com/gmail/api/quickstart/python) to get credentials for sending mails.  
Change `mailer_config.py` to modify (if there's any change) the file names of Google API Credentials.

# How to Run

> python2.7 main.py
