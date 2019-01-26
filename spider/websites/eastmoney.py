import traceback

import requests
from bs4 import BeautifulSoup
import json

from spider.website import WebSite


class EastmoneyReport(WebSite):

    def __init__(self):
        self.domain = "eastmoney"
        self.category = "report"
        super().__init__()

    def topic_wizard(self, code: str, page_num: int):
        return "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR" \
               "&code={}&p={}&ps=25&rt=51342638&js=%22data%22:[(x)],%22pages%22:%22(pc)%22," \
               "%22update%22:%22(ud)%22,%22count%22:%22(count)%22".format(code, page_num)

    def get_topics_by_page(self, page: dict):
        links = []
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "utf-8"
            data = json.loads("{" + r.text.strip().lstrip("(").rstrip(")") + "}")
            links = data.get("data", [])
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
        return [dict(domain=page["domain"],
                     url="http://data.eastmoney.com/report/{}/{}.html"
                     .format(d.get("datetime")[:10].replace("-", ""), d.get("infoCode", "")),
                     code=page.get("code", ""),
                     title=d.get("title"),
                     content="",
                     date=d.get("datetime").replace("T", " "),
                     org=d.get("insName"),
                     author=d.get("author"),
                     classify="",
                     category=page.get("category", ""))
                for d in links]

    def get_pages_by_code(self, code: str):
        page = self.first_page(code)
        pages = [page]
        try:
            r = requests.get(page["url"], headers=self.headers, timeout=5)
            r.encoding = "utf-8"
            data = json.loads("{" + r.text.strip().lstrip("(").rstrip(")") + "}")
            max_page = int(data.get("pages", 1))
            for i in range(2, max_page + 1):
                pages.append(dict(domain=self.domain,
                                  url=self.topic_wizard(code, i),
                                  code=code,
                                  category=self.category))
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        except json.decoder.JSONDecodeError:
            traceback.print_exc()
        except ValueError:
            traceback.print_exc()
        return pages

    def get_article_detail(self, article: dict):
        try:
            r = requests.get(article["url"], headers=self.headers, timeout=5)
            r.encoding = "gb2312"
            soup = BeautifulSoup(r.text, "html.parser")
            div = soup.find("div", "newsContent")
            # content
            content = div.text.strip() if div else ""
            article["content"] = content
        except KeyError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        return article


if __name__ == '__main__':
    job = EastmoneyReport()
    print(job.tag)
    p = job.first_page("600597")
    t = job.get_topics_by_page(p)
    print(t[0])
    print(job.get_article_detail(t[0]))
