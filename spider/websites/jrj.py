import re
import traceback

import requests
import urllib3
from bs4 import BeautifulSoup

from spider.website import WebSite


class JrjReport(WebSite):

    def __init__(self):
        self.domain = "jrj"
        self.category = "report"
        super().__init__()

    def topic_wizard(self, code: str, page_num: int):
        return "http://istock.jrj.com.cn/yanbao_{}_p{}.html".format(code, page_num)

    def get_topics_by_page(self, page: dict):
        links = []
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            url_expr = re.compile("http://istock.jrj.com.cn/article,yanbao,\d+.html")
            links = soup.find_all("a", href=url_expr)
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return [dict(domain=page.get("domain", ""),
                     url=link.get("href"),
                     code=page.get("code"),
                     title=link.get("title"),
                     content="",
                     date="",
                     org="",
                     author="",
                     classify="",
                     category=page.get("category"))
                for link in links]

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [page]
        try:
            r = requests.get(page["url"], timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            dom = soup.find_all("p", class_="page")
            dom = dom[-1].find_all("a") if dom else None
            if dom:
                page_expr = re.compile("(?<=p)\d+(?=.html)")
                matches = [int(page_expr.search(d.get("href")).group())
                           for d in dom
                           if d.get("href") and page_expr.search(d.get("href"))]
                max_page_num = max(matches) if matches else 1
                for i in range(2, max_page_num + 1):
                    pages.append(dict(domain=self.domain,
                                      url=self.topic_wizard(code, i),
                                      code=code,
                                      category=self.category))
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return pages

    def get_article_detail(self, article: dict):
        try:
            r = requests.get(article["url"], headers=self.headers, timeout=5)
            r.encoding = "gb2312"
            soup = BeautifulSoup(r.text, "html.parser")
            # content
            div = soup.find("div", id="replayContent")
            div = div.find_all("div", limit=1) if div else None
            content = div[0].text.strip() if div else ""
            article["content"] = content
            # author, date
            div = soup.find("div", class_="lou")
            div = div.find("p", class_="title") if div else None
            if div:
                if div.find("span"):
                    div.find("span").decompose()
                    author = div.find("a").text if div.find("a") else ""
                    article["author"] = author
                if div.find("a"):
                    div.find("a").decompose()
                    date = div.text.strip().lstrip("发表于").strip()
                    article["date"] = date
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        except requests.exceptions.ConnectionError:
            traceback.print_exc()
        except urllib3.exceptions.ReadTimeoutError:
            traceback.print_exc()
        return article


class JrjNews(WebSite):

    def __init__(self):
        super().__init__()
        self.domain = "jrj"
        self.category = "news"

    def topic_wizard(self, code: str, page_num: int):
        return "http://stock.jrj.com.cn/share,{},ggxw_{}.shtml".format(code, page_num)

    def first_page(self, code: str) -> dict:
        return dict(domain=self.name,
                    url=self.topic_wizard(code, 1).replace("ggxw_1", "ggxw"),
                    code=code,
                    category=self.category)

    def get_topics_by_page(self, page: dict):
        links = []
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            url_expr = re.compile("http://stock.jrj.com.cn/\d{4}/\d{2}/\d+.shtml")
            links = soup.find_all("a", href=url_expr)
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return [dict(domain=page.get("domain", ""),
                     url=link.get("href"),
                     code=page.get("code", ""),
                     title=link.text,
                     content="",
                     date=link.find_parent("span").text,
                     org="",
                     author="",
                     classify="",
                     category=page.get("category", ""))
                for link in links]

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [page]
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            dom = soup.find_all("p", class_="page_newslib")
            dom = dom[-1].find_all("a") if dom else None
            if dom:
                page_expr = re.compile("(?<=ggxw_)\d+(?=.shtml)")
                matches = [int(page_expr.search(d.get("href")).group())
                           for d in dom
                           if d.get("href") and page_expr.search(d.get("href"))]
                max_page_num = max(matches) if matches else 1
                for i in range(2, max_page_num + 1):
                    pages.append(dict(domain=self.name,
                                      url=self.topic_wizard(code, i),
                                      code=code,
                                      category=self.category))
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return pages

    def get_article_detail(self, article: dict):
        try:
            r = requests.get(article["url"], headers=self.headers, timeout=5)
            r.encoding = "gb2312"
            soup = BeautifulSoup(r.text, "html.parser")
            # content
            content = ""
            div = soup.find("div", class_="texttit_m1")
            for d in div.find_all("p") if div else []:
                if "class" not in d.attrs:
                    content += d.text.strip()
            article["content"] = content
            # org, date
            div = soup.find("p", class_="inftop")
            div = [d.text.strip() for d in div.find_all("span")] if div else []
            if div:
                date = div[0]
                article["date"] = date
                div = [d for d in div if "来源：" in d]
                org = div[0].lstrip("来源：") if div else ""
                article["org"] = org
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return article


if __name__ == '__main__':
    job = JrjNews()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(t[0])
    print(job.get_article_detail({"url": "http://stock.jrj.com.cn/2019/01/18000026924486.shtml"}))
