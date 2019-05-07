
import time


def api_exception_handler(func):
    def f(*args, **kwargs):
        r = func(*args, **kwargs)

        if r.status_code == 429:
            time.sleep(int(r.headers['retry-after']))
            api_exception_handler(func)(*args, *kwargs)

        if r.status_code != 200:
            raise ZendeskError(f"Zendesk API ERROR: {r.status_code}")

        return r.json()
    return f


class ZendeskError(BaseException):
    def __init__(self, kwargs):
        super().__init__(self, kwargs)
