import re
import traceback

import requests
from bs4 import BeautifulSoup
import json

from noodle.scrapy.domain import Domain
from noodle.scrapy.entity import Page, Article


class EastmoneyReport(Domain):

    def __init__(self):
        super().__init__()
        self.domain = "eastmoney"
        self.category = "report"

    def topic_wizard(self, code: str, page_num: int):
        return "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR" \
               "&code={}&p={}&ps=25&rt=51342638&js=%22data%22:[(x)],%22pages%22:%22(pc)%22," \
               "%22update%22:%22(ud)%22,%22count%22:%22(count)%22".format(code, page_num)

    def get_topics_by_page(self, page: Page):
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return []
        r.encoding = "utf-8"
        try:
            data = json.loads("{" + r.text.strip().lstrip("(").rstrip(")") + "}")
            return [Article(domain=page.domain,
                            url="http://data.eastmoney.com/report/{}/{}.html"
                            .format(d.get("datetime")[:10].replace("-", ""), d.get("infoCode", "")),
                            code=page.code,
                            title=d.get("title"),
                            content="",
                            date=d.get("datetime").replace("T", " "),
                            org=d.get("insName"),
                            author=d.get("author"),
                            classify="",
                            category=page.category)
                    for d in data.get("data", [])]
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
            print(r.text.strip())
            return []

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [self.first_page(code)]
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return pages
        r.encoding = "utf-8"
        try:
            data = json.loads("{" + r.text.strip().lstrip("(").rstrip(")") + "}")
            max_page = int(data.get("pages", 1))
            for i in range(2, max_page + 1):
                pages.append(Page(domain=self.domain,
                                  url=self.topic_wizard(code, i),
                                  code=code,
                                  category=self.category))
            return pages
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
            return pages

    def get_article_detail(self, article: Article):
        try:
            r = requests.get(article.url, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            traceback.print_exc()
            return article
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", "newsContent")
        content = ""
        if div:
            # content
            content = div.text.strip()
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
    job = EastmoneyReport()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(job.get_article_detail(t[0]))
    print(len(job.get_topics_by_code("600597")))