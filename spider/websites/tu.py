import traceback

import tushare as ts

from spider.website import WebSite


class TushareNews(WebSite):

    def __init__(self):
        self.domain = "tushare"
        self.category = "news"
        super().__init__()

    def get_topics(self):
        links = []
        df = ts.get_latest_news(top=2000, show_content=False)
        links = df.to_dict(orient="records") if df is not None else []
        return [dict(domain=self.domain,
                     url=d.get("url"),
                     code="",
                     title=d.get("title"),
                     content="",
                     date=d.get("time"),
                     org="",
                     author="",
                     classify=d.get("classify"),
                     category=self.category)
                for d in links]

    def get_article_detail(self, article: dict):
        try:
            content = ts.latest_content(article["url"])
            content = content.strip() if content else ""
            article["content"] = content
        except KeyError:
            traceback.print_exc()
        return article


if __name__ == '__main__':
    job = TushareNews()
    t = job.get_topics()
    print(job.get_article_detail(t[0]))
