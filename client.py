from .request import ZendeskRequest
from urllib.parse import quote


class Zendesk():
    def __init__(self, instance, helpcenter, auth):
        self.__client = ZendeskClient(instance, auth)
        self.__helpcenter = ZendeskHC(helpcenter, auth)

    @property
    def client(self):
        return self.__client

    @property
    def helpcenter(self):
        return self.__helpcenter


class ZendeskHC(ZendeskRequest):
    __articles_endpoint__ = 'articles'
    __articles_key__ = 'articles'
    __categories_endpoint__ = 'categories'
    __categories_key__ = 'categories'
    __sections_endpoint__ = 'sections'
    __sections_key__ = 'sections'
    __user_segments_endpoint__ = 'user_segments'
    __user_segments_key__ = 'user_segments'
    __per_page__ = 1000

    def __init__(self, url, auth):
        super().__init__(url, auth, prefix='hc')

    def __get_per_page_param(self):
        return {'per_page': self.__per_page__}

    def articles(self, category_id=None, include=None):
        params = self.__get_per_page_param()
        keys = [self.__articles_key__]
        if include:
            params.update({'include': include})
            keys = keys+include.split(',')
        if category_id:
            target_endpoint = f"categories/{category_id}/{self.__articles_endpoint__}"
        else:
            target_endpoint = self.__articles_endpoint__
        return super().__get__(target_endpoint, keys=keys, params=params)

    def update_article_title(self, article_id, title, locale):
        data = {'translation': {'title': title}}
        return super().__put__(f'articles/{article_id}/translations/{locale}.json', data)

    def categories(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__categories_endpoint__, keys=[self.__categories_key__], params=params)

    def sections(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__sections_endpoint__, keys=[self.__sections_key__], params=params)

    def user_segments(self):
        params = self.__get_per_page_param()
        return super().__get__(self.__user_segments_endpoint__, keys=[self.__user_segments_key__], params=params)


class ZendeskClient(ZendeskRequest):
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

    def __init__(self, url, token):
        super().__init__(url, token)

    def permission_groups(self):
        return super().__get__(self.__permission_groups_endpoint__, keys=[self.__permission_groups_key__], params=None)

    def users(self):
        return super().__get__(self.__users_endpoint__, keys=[self.__users_key__], params=None)

    def brands(self):
        return super().__get__(self.__brands_endpoint__, keys=[self.__brands_key__], params=None)

    def brand(self, id):
        target_endpoint = f'{self.__brands_endpoint__}/{str(id)}'
        return super().__get__(target_endpoint, keys=[self.__brand_key__], params=None)

    def ticket_fields(self):
        return super().__get__(self.__ticket_fields_endpoint__, keys=[self.__ticket_fields_key__], params=None)

    def search(self, query):
        params = {
            'query': query,
            'per_page': self.__per_page__}
        return super().__get__(self.__search_endpoint__, keys=[self.__search_key__], params=params)
