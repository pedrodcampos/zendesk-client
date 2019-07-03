from . import oauth
from .helpcenter import ZendeskHC
from .support import ZendeskSupport


class ZendeskClient:
    def __init__(self, url, auth, auth_method="token"):
        self.__url = url
        self.__auth = auth
        self.__auth_method = auth_method
        self.support = ZendeskSupport(url, auth, auth_method)
        self.helpcenter = self.get_helpcenter

    def get_helpcenter(self, brand_id):
        brand = self.support.brands(brand_id)["brand"]

        return ZendeskHC(brand["brand_url"], self.__auth, self.__auth_method)
