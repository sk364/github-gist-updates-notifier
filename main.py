#!/usr/bin/python2.7
"""
Description: GitHub Gists' Updates Notifier
Author: Sachin Kukreja
"""

import os
import time
from datetime import datetime

import requests

from config import ACCESS_TOKEN, API_LINK, RECIPIENTS
from mailer import send_mail


def notify():
    """
    Monitors authenticated user's starred gists.
    Sends mail if there is any update in the gist.
    """

    req_obj = requests.get(
        API_LINK.format('gists/starred'),
        params={'since': LAST_UPDATED_AT, 'per_page': 100},
        headers={'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}
    )

    if req_obj.status_code == 200:
        starred_gists = req_obj.json()
        gist_urls = []

        if LAST_UPDATED_AT:
            max_updated_at = datetime.strptime(LAST_UPDATED_AT, '%Y-%m-%dT%H:%M:%SZ')
        else:
            max_updated_at = datetime(2000, 1, 1, 23, 59, 59)

        last_updated_at = max_updated_at

        for gist in starred_gists: 
            updated_at = datetime.strptime(gist['updated_at'], '%Y-%m-%dT%H:%M:%SZ')

            if updated_at > last_updated_at:
                gist_urls.append(gist['html_url'])

            if updated_at > max_updated_at:
                max_updated_at = updated_at

        if gist_urls:
            send_mail(recipients=RECIPIENTS, subject='Updates in Gists', body=', '.join(gist_urls))
            print 'Mail Sent...'

            with open(os.path.join(BASE_DIR, '.last_timestamp'), 'w') as f:
                f.write(max_updated_at.strftime('%Y-%m-%dT%H:%M:%SZ'))
    else:
        print req_obj.status_code, req_obj.content


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(BASE_DIR, '.last_timestamp')) is False:
        with open(os.path.join(BASE_DIR, '.last_timestamp'), 'w') as f:
            f.write('')

    sleep_time = 120
    print 'Daemon running...'

    while True:
        with open(os.path.join(BASE_DIR, '.last_timestamp')) as f:
            LAST_UPDATED_AT = f.read()

        notify()

        print 'Sleeping...'
        time.sleep(sleep_time)

        sleep_time = sleep_time * 2
        if sleep_time > 21600:              # reset sleep time if more than 6 hours
            sleep_time = 120

