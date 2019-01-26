import re
import traceback

import requests
from bs4 import BeautifulSoup

from spider.website import WebSite


class SinaReport(WebSite):

    def __init__(self):
        self.domain = "sina"
        self.category = "report"
        super().__init__()

    def topic_wizard(self, code: str, page_num: int):
        return "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?symbol=" \
               "{}&t1=all&p={}".format(code, page_num)

    def get_topics_by_page(self, page: dict):
        links = []
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "gb2312"
            soup = BeautifulSoup(r.text, "html.parser")
            url_expr = re.compile("vip.stock.finance.sina.com.cn/q/go.php/vReport_Show/kind/search/rptid")
            links = soup.find_all("a", href=url_expr)
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return [dict(domain=page.get("domain",""),
                     url=link.get("href"),
                     code=page.get("code",""),
                     title=link.get("title"),
                     content="",
                     date="",
                     org="",
                     author="",
                     classify="",
                     category=page.get("category", ""))
                for link in links]

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [page]
        try:
            r = requests.get(page["url"],  headers=self.headers, timeout=5)
            r.encoding = "gb2312"
            soup = BeautifulSoup(r.text, "html.parser")
            dom = soup.find_all("a", onclick=re.compile("set_page_num"))
            if dom:
                last_onclick = dom[-1].get("onclick")
                match = re.search("(?<=set_page_num\(')(.*)?(?='\))", last_onclick)
                max_page_num = int(match.group()) if match else 1
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
            dom = soup.find("div", class_="content")
            if dom:
                # title
                div = dom.find("h1")
                title = div.text.strip() if div else ""
                article["title"] = title
                # content
                div = dom.find("div", class_="blk_container")
                content = div.text.strip() if div else ""
                article["content"] = content
                # author org date
                div = dom.find("div", class_="creab")
                if div:
                    spans = [d.text.strip() for d in div.findAll("span")]
                    authors = [span for span in spans if "研究员：" in span]
                    author = authors[0].lstrip("研究员：") if authors else ""
                    article["author"] = author
                    orgs = [span for span in spans if "机构：" in span]
                    org = orgs[0].lstrip("机构：") if orgs else ""
                    article["org"] = org
                    dates = [span for span in spans if "日期：" in span]
                    date = dates[0].lstrip("日期：") if dates else ""
                    article["date"] = date
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return article


if __name__ == '__main__':
    job = SinaReport()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(t[0])
    print(job.get_article_detail(t[0]))
