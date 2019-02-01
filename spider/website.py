class WebSite(object):

    domain = ""
    category = ""
    max_page = 50
    tag = ""

    def __init__(self):
        self.tag = self.domain + "_" + self.category

    @property
    def headers(self):
        return {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE7.0; WindowsNT5.1; Maxthon2.0)"
        }

    def topic_wizard(self, code: str, page_num: int) -> str:
        """
        返回目录页 url
        :param code:
        :param page_num:
        :return:
        """
        pass

    def first_page(self, code: str) -> dict:
        """
        返回目录页首页 url
        :param code:
        :return:
        """
        return dict(domain=self.domain,
                    url=self.topic_wizard(code, 1),
                    code=code,
                    category=self.category)

    def get_pages_by_code(self, code: str) -> list:
        """
        返回全部页
        :param code:
        :return:
        """
        pass

    def get_topics_by_page(self, page: dict) -> list:
        """
        返回当前页全部文章
        :param page:
        :return:
        """
        pass

    def get_topics_by_code(self, code: str) -> list:
        """
        返回当前code全部文章
        :param code:
        :return:
        """
        topics = []
        pages = self.get_pages_by_code(code)
        for page in pages:
            topics.extend(self.get_topics_by_page(page))
        return topics

    def get_article_detail(self, article: dict) -> dict:
        """
        返回文文章详情
        :param article:
        :return:
        """
        pass

    def get_topics(self) -> list:
        """
        返回无CODE目录
        :return:
        """
        pass

    def get_info(self, code: str) -> list:
        """
        返回CODE详情
        :param code:
        :return:
        """
        pass

    def get_balance(self, code: str) -> list:
        """
        返回资产负债表
        :param code:
        :return:
        """
        pass

    def get_cashflow(self, code: str) -> list:
        """
        返回现金流量表
        :param code:
        :return:
        """
        pass

    def get_profit(self, code: str) -> list:
        """
        返回利润表
        :param code:
        :return:
        """
        pass

    def get_summary(self, code: str) -> list:
        """
        返回财务摘要
        :param code:
        :return:
        """
        pass
