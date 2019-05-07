import json
import os
import requests


def load_instances():
    file_path = os.path.join(os.curdir, 'instances.json')
    with open(file_path) as f:
        return json.load(f)


class ZendeskOAuth():
    auth_url = None
    token_request_url = None
    revoke_access_url = None
    logout_url = None

    def __init__(self, name, url, client_id, secret_key, redirect_uri):
        self.name = name
        self.url = url
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.__build_urls()

    def __build_urls(self):
        self.auth_url = self.url + "/oauth/authorizations/new"
        self.token_request_url = self.url + "/oauth/tokens"
        self.revoke_access_url = self.url + "/api/v2/oauth/tokens/current"
        self.logout_url = self.url + "/access/logout"

    def auth_request_url(self):

        params = {'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'client_id': self.client_id,
                  'scope': 'read write'}

        req = requests.PreparedRequest()
        req.prepare_url(self.auth_url, params)
        return req.url

    def get_token(self, auth_code):

        params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.secret_key,
            'redirect_uri': self.redirect_uri,
            'scope': 'read write'
        }

        response = requests.post(self.token_request_url, data=params)
        if response.status_code == 200:
            r = response.json()
            return r['access_token']

    def revoke_access(self, token):
        headers = {"Authorization": f'Bearer {token}'}
        requests.delete(self.revoke_access_url, headers=headers)
