import json
import traceback

import requests
from bs4 import BeautifulSoup

from spider.website import WebSite


class WangyiReport(WebSite):

    def __init__(self):
        self.domain = "163"
        self.category = "report"
        super().__init__()

    def topic_wizard(self, code: str, page_num: int):
        code = "sh{}".format(code) if code>"600000" else "sz{}".format(code)
        return "http://163.vguwang.com/pubapi1/get_gp_news_lists?" \
               "page={}&page_size=20&symbol={}&type=yanbao".format(page_num, code)

    def get_topics_by_page(self, page: dict):
        links = []
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "utf-8"
            data = r.json()
            links = data["data"]
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
        return [dict(domain=page.get("domain", ""),
                     url="http://163.vguwang.com/gp/news_view?id={}".format(link.get("id")),
                     code=page.get("code", ""),
                     title=link.get("title"),
                     content="",
                     date=link.get("create_time", ""),
                     org=link.get("sources", ""),
                     author=link.get("author", ""),
                     classify="",
                     category=page.get("category", ""))
                for link in links]

    def get_pages_by_code(self, code: str):
        pages = []
        for i in range(1, self.max_page):
            try:
                r = requests.get(self.topic_wizard(code, i), headers=self.headers, timeout=5)
                r.encoding = "utf-8"
                data = r.json()
                if not data.get("data", []):
                    break
                else:
                    pages.append(dict(domain=self.domain,
                                      url=self.topic_wizard(code, i),
                                      code=code,
                                      category=self.category))
            except requests.Timeout:
                traceback.print_exc()
                break
            except json.decoder.JSONDecodeError:
                traceback.print_exc()
                break
        return pages

    def get_article_detail(self, article: dict):
        try:
            r = requests.get(article["url"], headers=self.headers, timeout=5)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            div = soup.find("div", id="news_content")
            content = div.text.strip() if div else ""
            article["content"] = content
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return article


if __name__ == '__main__':
    job = WangyiReport()
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(t[0])
    print(job.get_article_detail(t[0]))
