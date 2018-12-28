import tushare as ts

from noodle.spider.domain import Domain
from noodle.spider.entity import Article


class TushareNews(Domain):

    def __init__(self):
        super().__init__()
        self.domain = "tushare"
        self.category = "news"

    def get_topics(self):
        df = ts.get_latest_news(top=2000, show_content=False)
        if df is not None:
            return [Article(domain=self.domain,
                            url=d.get("url"),
                            code="",
                            title=d.get("title"),
                            content="",
                            date=d.get("time"),
                            org="",
                            author="",
                            classify=d.get("classify"),
                            category=self.category)
                    for d in df.to_dict(orient="records")]
        else:
            return []

    def get_article_detail(self, article: Article):
        content = ts.latest_content(article.url)
        if content:
            content = content.strip()
        else:
            content = ""
        return Article(domain=article.domain,
                       url=article.url,
                       code=article.code,
                       title=article.title,
                       content=content,
                       date=article.date,
                       org=article.org,
                       author=article.author,
                       classify=article.classify,
                       category=article.category)


if __name__ == '__main__':
    job = TushareNews()
    t = job.get_topics()
    print(job.get_article_detail(t[0]))