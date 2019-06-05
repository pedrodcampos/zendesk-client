import requests
import time
from urllib.parse import (parse_qs, urlsplit,
                          urlunsplit, urlencode)

from ..exceptions import ZendeskError, api_exception_handler
from .helpers import reduce_dict, append_param_to_url


class ZendeskRequest:
    def __init__(self, url, auth, auth_method='token', prefix=None):
        self.__url = url
        self.__session = requests.Session()
        self.__version = 'v2'
        self.__prefix = prefix

        if auth_method.lower() == 'token':
            self.__session.headers['Authorization'] = f"Bearer {auth}"
        elif auth_method.lower() == 'password':
            self.__session.auth = auth
        else:
            raise ZendeskError('Invalid Authentication method.')

    @api_exception_handler
    def put(self, endpoint, data=None):
        endpoint_parts = endpoint.split('/')
        url = self.__get_enpoint_url(
            *endpoint_parts)
        self.__session.headers.update({"Accept": "application/json"})
        self.__session.headers.update({"Content-type": "application/json"})
        response = self.__session.put(url, json=data)

        return response

    @api_exception_handler
    def post(self, endpoint, data=None):
        endpoint_parts = endpoint.split('/')
        url = self.__get_enpoint_url(
            *endpoint_parts)
        response = self.__session.post(url, data=data)
        return response

    @api_exception_handler
    def __get_page(self, endpoint, keys=None, params=None, parseEndpoint=True):
        if parseEndpoint:
            endpoint_parts = endpoint.split('/')
            url = self.__get_enpoint_url(
                *endpoint_parts)
            url = append_param_to_url(params, url)
        else:
            url = endpoint

        response = self.__session.get(url)
        return response

    def get(self, endpoint, keys=None, params=None, limit=None, progress_cb=None):
        data = {}
        if limit:
            params['per_page'] = limit
        while True:
            try:
                response = self.__get_page(
                    endpoint, keys, params, len(data) == 0)
            except Exception as e:
                progress_cb(status='error', error=e)

            for key in keys:
                if key in data:
                    data[key].extend(response.get(key, None))
                else:
                    data[key] = response.get(key, None)

                if progress_cb:
                    progress_cb(status='working',
                                key=key,
                                progress=100*len(data[key])/response.get(
                                    'count', None),
                                total=response.get('count', None),
                                current=len(data[key]))

            if limit:
                break
            endpoint = response.get('next_page', None)
            if endpoint:
                if params:
                    endpoint = append_param_to_url(params, endpoint)
            else:
                break

        for key in keys:
            if key in data:
                data[key] = reduce_dict(data[key])

        if progress_cb:
            progress_cb(status='done',
                        total=response.get('count', None),
                        current=len(data))
        return data

    def __get_enpoint_url(self, *args):
        path = [self.__url]
        if self.__prefix:
            path.append(self.__prefix)
        path.append('api')
        path.append(self.__version)
        path = path + list(args)
        path = "/".join(map(str, path))
        return f"{path}"

    def __reduce(self, data):
        if type(data) == list:
            reduced = {}
            for item in data:
                item_id = item['id']
                reduced.update({item_id: item})
            return [item for item in reduced.values()]
        return data
