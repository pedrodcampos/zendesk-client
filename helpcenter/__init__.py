from request import ZendeskRequest


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
