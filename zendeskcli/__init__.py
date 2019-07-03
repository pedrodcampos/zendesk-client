from . import oauth
from .helpcenter import ZendeskHC
from .support import ZendeskSupport


class ZendeskClient:
    def __init__(self, url, auth, auth_method='token'):
        self.support = ZendeskSupport(url, auth, auth_method)
        self.helpcenter = ZendeskHC(url, auth, auth_method)
