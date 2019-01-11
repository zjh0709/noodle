from spider.entity import Article, Page


class Domain(object):

    def __init__(self):
        self.domain = ""
        self.category = ""
        self.max_page = 50

    @property
    def headers(self):
        return {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE7.0; WindowsNT5.1; Maxthon2.0)"
        }

    def topic_wizard(self, code: str, page_num: int) -> str:
        pass

    def first_page(self, code: str) -> Page:
        return Page(domain=self.domain,
                    url=self.topic_wizard(code, 1),
                    code=code,
                    category=self.category)

    def get_pages_by_code(self, code: str) -> list:
        pass

    def get_topics_by_page(self, page: Page) -> list:
        pass

    def get_topics_by_code(self, code: str) -> list:
        topics = []
        pages = self.get_pages_by_code(code)
        for page in pages:
            topics.extend(self.get_topics_by_page(page))
        return topics

    def get_article_detail(self, article: Article) -> Article:
        pass

    def get_topics(self):
        pass

    def get_info(self, code: str):
        pass
