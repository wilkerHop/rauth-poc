#!/usr/bin/env python

import hashlib
import os
import sys
from rauth import OAuth2Service
from urllib.parse import parse_qsl

if sys.version_info[0] == 3:
    raw_input = input

client_id = raw_input('Enter your App Id: ')
secret = raw_input('Enter your App Secret: ')

service = OAuth2Service(
    client_id=client_id,  # your App ID from https://wakatime.com/apps
    client_secret=secret,  # your App Secret from https://wakatime.com/apps
    name='wakatime',
    authorize_url='https://wakatime.com/oauth/authorize',
    access_token_url='https://wakatime.com/oauth/token',
    base_url='https://wakatime.com/api/v1/')

redirect_uri = 'https://wakatime.com/oauth/test'
state = hashlib.sha1(os.urandom(40)).hexdigest()
params = {'scope': 'email,read_stats',
          'response_type': 'code',
          'state': state,
          'redirect_uri': redirect_uri}

url = service.get_authorize_url(**params)

print('**** Visit this url in your browser ****'.format(url=url))
print('*' * 80)
print(url)
print('*' * 80)
print('**** After clicking Authorize, paste code here and press Enter ****')
code = raw_input('Enter code from url: ')

# Make sure returned state has not changed for security reasons, and exchange
# code for an Access Token.
headers = {'Accept': 'application/x-www-form-urlencoded'}
print('Getting an access token...')
session = service.get_auth_session(headers=headers,
                                   data={'code': code,
                                         'grant_type': 'authorization_code',
                                         'redirect_uri': redirect_uri})
print(session.access_token)
print(dict(parse_qsl(session.access_token_response.text))['refresh_token'])
