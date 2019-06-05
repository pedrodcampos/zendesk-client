from ..request import ZendeskRequest


class ZendeskSupport():
    __permission_groups_keys__ = ['permission_groups']
    __permission_groups_endpoint__ = 'guide/permission_groups'
    __users_keys__ = ['users', 'user']
    __users_endpoint__ = 'users'
    __brands_keys__ = ['brands', 'brand']
    __brands_endpoint__ = 'brands'
    __search_endpoint__ = 'search'
    __search_keys__ = ['results']
    __ticket_fields_endpoint__ = 'ticket_fields'
    __ticket_fields_keys__ = ['ticket_fields']
    __per_page__ = 1000

    def __init__(self, url, auth, auth_method):
        self.__request = ZendeskRequest(url, auth, auth_method)

    def permission_groups(self):
        return self.__request.get(self.__permission_groups_endpoint__, keys=self.__permission_groups_keys__, params=None)

    def users(self, id=None):
        target_endpoint = self.__users_endpoint__
        if id:
            target_endpoint += f'/{str(id)}'
        return self.__request .get(target_endpoint, keys=self.__users_keys__, params=None)

    def brands(self, id=None):
        target_endpoint = self.__brands_endpoint__
        if id:
            target_endpoint += f'/{str(id)}'
        return self.__request .get(target_endpoint, keys=self.__brands_keys__, params=None)

    def ticket_fields(self):
        return self.__request.get(self.__ticket_fields_endpoint__, keys=self.__ticket_fields_keys__, params=None)

    def search(self, query, limit=None, progress_cb=None):
        params = {
            'query': query,
            'per_page': self.__per_page__}
        return self.__request.get(self.__search_endpoint__, keys=self.__search_keys__, params=params, limit=limit, progress_cb=progress_cb)
