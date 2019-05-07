
from urllib.parse import (parse_qs, urlsplit,
                          urlunsplit, urlencode)


def append_param_to_url(params, url):

    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    if params:
        for param in params:
            query_params.update(param)
    query_params = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path,  query_params, fragment))


def reduce_dict(data):
    if type(data) == list:
        reduced = {}
        for item in data:
            item_id = item['id']
            reduced.update({item_id: item})
        return [item for item in reduced.values()]
    return data
