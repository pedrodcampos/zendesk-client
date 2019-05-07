import requests
import time
from urllib.parse import urlparse, urlunparse, parse_qs, urlsplit, urlunsplit, urlencode


class ZendeskRequest:
    def __init__(self, url, token, prefix=None):
        self.__url = url
        self.__session = requests.Session()
        self.__session.headers['Authorization'] = f"Bearer {token}"
        self.__version = 'v2'
        self.__prefix = prefix

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

    def __put__(self, endpoint, data=None):
        endpoint_parts = endpoint.split('/')
        url = self.__get_enpoint_url(
            *endpoint_parts)
        self.__session.headers.update({"Accept": "application/json"})
        self.__session.headers.update({"Content-type": "application/json"})
        response = self.__session.put(url, json=data)

        if response.status_code != 200:
            raise BaseException(f"Zendesk API Error:{response.status_code}")

        response = response.json()
        return response

    def __post__(self, endpoint, data=None):
        endpoint_parts = endpoint.split('/')
        url = self.__get_enpoint_url(
            *endpoint_parts)
        response = self.__session.post(url, data=data)

        if response.status_code != 200:
            raise BaseException(f"Zendesk API Error:{response.status_code}")

        response = response.json()
        return response

    def __get__(self, endpoint, keys=None,  params=None):
        data = {}
        endpoint_parts = endpoint.split('/')
        url = self.__get_enpoint_url(
            *endpoint_parts)+('?'+urlencode(params) if params else "")

        while url:
            response = self.__session.get(url)

            if response.status_code != 200:
                raise BaseException(
                    f"Zendesk API Error:{response.status_code}")

            if response.status_code == 429:
                print('Rate limited! Please wait.')
                time.sleep(int(response.headers['retry-after']))
                continue

            response = response.json()

            for key in keys:
                if key in data:
                    data[key].extend(response.get(key, None))
                else:
                    data[key] = response.get(key, None)

            count = response.get('count', None)
            print(f'Got {len(data[keys[0]])}/{count}')

            url = response.get('next_page', None)
            if url:
                url = self.__append_param_to_url(params, url)

        for key in keys:
            if key in data:
                data[key] = self.__reduce(data[key])

        return data.values()

    def __append_param_to_url(self, param, url):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)

        query_params.update(param)
        new_query_string = urlencode(query_params, doseq=True)

        return urlunsplit((scheme, netloc, path, new_query_string, fragment))
