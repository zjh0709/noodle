import re
import traceback

import requests
from bs4 import BeautifulSoup

from noodle.scrapy.domain import Domain
from noodle.scrapy.entity import Page, Article


class SinaReport(Domain):

    def __init__(self):
        super().__init__()
        self.domain = "sina"
        self.category = "report"

    def topic_wizard(self, code: str, page_num: int):
        return "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?symbol=" \
               "{}&t1=all&p={}".format(code, page_num)

    def get_topics_by_page(self, page: Page):
        url_expr = re.compile("vip.stock.finance.sina.com.cn/q/go.php/vReport_Show/kind/search/rptid")
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return []
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=url_expr)
        return [Article(domain=page.domain,
                        url=link.get("href"),
                        code=page.code,
                        title=link.get("title"),
                        content="",
                        date="",
                        org="",
                        author="",
                        classify="",
                        category=page.category)
                for link in links]

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [self.first_page(code)]
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return pages
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        dom = soup.find_all("a", onclick=re.compile("set_page_num"))
        if dom:
            last_onclick = dom[-1].get("onclick")
            match = re.search("(?<=set_page_num\(')(.*)?(?='\))", last_onclick)
            max_page_num = int(match.group()) if match else 1
            for i in range(2, max_page_num + 1):
                pages.append(Page(domain=self.domain,
                                  url=self.topic_wizard(code, i),
                                  code=code,
                                  category=self.category))
        return pages

    def get_article_detail(self, article: Article):
        try:
            r = requests.get(article.url, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            traceback.print_exc()
            return article
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        dom = soup.find("div", class_="content")
        content, title, author, org, date = "", "", "", "", ""
        if dom:
            # title
            div = dom.find("h1")
            if div:
                title = div.text.strip()
            # content
            div = dom.find("div", class_="blk_container")
            if div:
                content = div.text.strip()
            # author org date
            div = dom.find("div", class_="creab")
            if div:
                spans = [d.text.strip() for d in div.findAll("span")]
                authors = [span for span in spans if "研究员：" in span]
                if authors:
                    author = authors[0].lstrip("研究员：")
                orgs = [span for span in spans if "机构：" in span]
                if orgs:
                    org = orgs[0].lstrip("机构：")
                dates = [span for span in spans if "日期：" in span]
                if dates:
                    date = dates[0].lstrip("日期：")
        return Article(domain=article.domain,
                       url=article.url,
                       code=article.code,
                       title=title,
                       content=content,
                       date=date,
                       org=org,
                       author=author,
                       classify=article.classify,
                       category=article.category)


if __name__ == '__main__':
    job = SinaReport()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(len(job.get_topics_by_code("600597")))