import re
import traceback

import requests
from bs4 import BeautifulSoup

from noodle.scrapy.domain import Domain
from noodle.scrapy.entity import Page, Article


class JrjReport(Domain):

    def __init__(self):
        super().__init__()
        self.domain = "jrj"
        self.category = "report"

    def topic_wizard(self, code: str, page_num: int):
        return "http://istock.jrj.com.cn/yanbao_{}_p{}.html".format(code, page_num)

    def get_topics_by_page(self, page: Page):
        url_expr = re.compile("http://istock.jrj.com.cn/article,yanbao,\d+.html")
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return []
        r.encoding = "gbk"
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
        r.encoding = "gbk"
        soup = BeautifulSoup(r.text, "html.parser")
        dom = soup.find_all("p", class_="page")
        page_expr = re.compile("(?<=p)\d+(?=.html)")
        if dom:
            dom = dom[-1].find_all("a")
            if dom:
                matches = [int(page_expr.search(d.get("href")).group())
                           for d in dom
                           if d.get("href") and page_expr.search(d.get("href"))]
                max_page_num = max(matches) if matches else 1
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
        # content
        content = ""
        div = soup.find("div", id="replayContent")
        if div:
            div = div.find_all("div", limit=1)
            if div:
                content = div[0].text.strip()
        # author, date
        author, date = "", ""
        div = soup.find("div", class_="lou")
        if div:
            div = div.find("p", class_="title")
            if div:
                div.find("span").decompose()
                author = div.find("a").text if div.find("a") else ""
                div.find("a").decompose()
                date = div.text.strip().lstrip("发表于").strip()
        return Article(domain=article.domain,
                       url=article.url,
                       code=article.code,
                       title=article.title,
                       content=content,
                       date=date,
                       org=article.org,
                       author=author,
                       classify=article.classify,
                       category=article.category)


class JrjNews(Domain):

    def __init__(self):
        super().__init__()
        self.name = "jrj"
        self.category = "news"

    def topic_wizard(self, code: str, page_num: int):
        return "http://stock.jrj.com.cn/share,{},ggxw_{}.shtml".format(code, page_num)

    def first_page(self, code: str) -> Page:
        return Page(domain=self.name,
                    url=self.topic_wizard(code, 1).replace("ggxw_1", "ggxw"),
                    code=code,
                    category=self.category)

    def get_topics_by_page(self, page: Page):
        url_expr = re.compile("http://stock.jrj.com.cn/\d{4}/\d{2}/\d+.shtml")
        try:
            r = requests.get(page.url, timeout=5)
        except requests.ConnectTimeout:
            traceback.print_exc()
            return []
        r.encoding = "gbk"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", href=url_expr)
        return [Article(domain=page.domain,
                        url=link.get("href"),
                        code=page.code,
                        title=link.text,
                        content="",
                        date=link.find_parent("span").text,
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
        r.encoding = "gbk"
        soup = BeautifulSoup(r.text, "html.parser")
        dom = soup.find_all("p", class_="page_newslib")
        page_expr = re.compile("(?<=ggxw_)\d+(?=.shtml)")
        if dom:
            dom = dom[-1].find_all("a")
            if dom:
                matches = [int(page_expr.search(d.get("href")).group())
                           for d in dom
                           if d.get("href") and page_expr.search(d.get("href"))]
                max_page_num = max(matches) if matches else 1
                for i in range(2, max_page_num + 1):
                    pages.append(Page(domain=self.name,
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
        # content
        content = ""
        div = soup.find("div", class_="texttit_m1")
        if div:
            for d in div.find_all("p"):
                if "class" not in d.attrs:
                    content += d.text.strip()
        # org, date
        org, date = "", ""
        div = soup.find("p", class_="inftop")
        if div:
            div = [d.text.strip() for d in div.find_all("span")]
        if div:
            date = div[0]
            div = [d for d in div if "来源：" in d]
            if div:
                org = div[0].lstrip("来源：")
        return Article(domain=article.domain,
                       url=article.url,
                       code=article.code,
                       title=article.title,
                       content=content,
                       date=date,
                       org=org,
                       author=article.author,
                       classify=article.classify,
                       category=article.category)


if __name__ == '__main__':
    job = JrjNews()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(job.get_article_detail(t[0]))
    # print(len(job.get_topics_by_code("600597")))
