from ..request import ZendeskRequest


class ZendeskSupport():
    __permission_groups_key__ = 'permission_groups'
    __permission_groups_endpoint__ = 'guide/permission_groups'
    __users_key__ = 'users'
    __users_endpoint__ = 'users'
    __brands_key__ = 'brands'
    __brand_key__ = 'brand'
    __brands_endpoint__ = 'brands'
    __search_endpoint__ = 'search'
    __search_key__ = 'results'
    __ticket_fields_endpoint__ = 'ticket_fields'
    __ticket_fields_key__ = 'ticket_fields'
    __per_page__ = 1000

    def __init__(self, url, auth, auth_method):
        self.__request = ZendeskRequest(url, auth, auth_method)

    def permission_groups(self):
        return self.__request.get(self.__permission_groups_endpoint__, keys=[self.__permission_groups_key__], params=None)

    def users(self):
        return self.__request .get(self.__users_endpoint__, keys=[self.__users_key__], params=None)

    def brands(self):
        return self.__request.get(self.__brands_endpoint__, keys=[self.__brands_key__], params=None)

    def brand(self, id):
        target_endpoint = f'{self.__brands_endpoint__}/{str(id)}'
        return self.__request .get(target_endpoint, keys=[self.__brand_key__], params=None)

    def ticket_fields(self):
        return self.__request.get(self.__ticket_fields_endpoint__, keys=[self.__ticket_fields_key__], params=None)

    def search(self, query, limit=None, progress_cb=None):
        params = {
            'query': query,
            'per_page': self.__per_page__}
        return self.__request.get(self.__search_endpoint__, keys=[self.__search_key__], params=params, limit=limit, progress_cb=progress_cb)
