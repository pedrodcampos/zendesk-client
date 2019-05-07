import json
import os
import requests


class ZendeskOAuth():
    __auth_endpoint = "{}/oauth/authorizations/new"
    __token_request_endpoint = "{}/oauth/tokens"
    __revoke_access_endpoint = "{}/api/v2/oauth/tokens/current"
    __logout_endpoint = "{}/access/logout"

    def __init__(self, name, url, client_id, secret_key, redirect_uri):
        self.name = name
        self.url = url
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.auth_url = self.__auth_endpoint.format(url)
        self.token_request_url = self.__token_request_endpoint.format(url)
        self.revoke_access_url = self.__revoke_access_endpoint.format(url)
        self.logout_url = self.__logout_endpoint.format(url)

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
