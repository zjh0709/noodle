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
        return [dict(domain=page.get("domain", ""),
                     url=link.get("href"),
                     code=page.get("code", ""),
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
            r = requests.get(page["url"], headers=self.headers, timeout=5)
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


class SinaInfo(WebSite):
    def __init__(self):
        self.domain = "sina"
        self.category = "info"
        super().__init__()

    def get_info(self, code: str):
        result = []
        # 行业、概念
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/{}/menu_num/2.phtml".format(
            code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            tables = soup.find_all("table", class_="comInfo1")
            for table in tables:
                bk = ""
                for idx, tr in enumerate(table.find_all("tr")):
                    if idx == 0:
                        if "所属" not in tr.text:
                            break
                        bk = tr.text.replace("所属", "").replace("板块", "").strip()
                    else:
                        if not bk:
                            break
                        tds = tr.find_all("td")
                        if len(tds) > 1:
                            result.append((bk, tds[0].text, ""))
        except requests.Timeout:
            traceback.print_exc()
        # 股东
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/{}/displaytype/30.phtml".format(
            code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find(id="Table1")
            is_start = False
            if table:
                for tr in table.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) == 5 and "编号" not in tds[0].text:
                        is_start = True
                        v = tds[1].text
                        o = re.search("[\d.]+", tds[3].text).group() if re.search("[\d.]+", tds[3].text) else ""
                        result.append(("股东", v, o + "%"))
                    elif len(tds) < 5 and is_start:
                        break
        except requests.Timeout:
            traceback.print_exc()
        return result

    def get_balance(self, code: str):
        result = []
        url = "http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{}/ctrl/part/displaytype/4.phtml".format(
            code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find(id="BalanceSheetNewTable0")
            o = ""
            if table:
                for tr in table.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) <= 1:
                        continue
                    n = tds[0].text
                    v = tds[1].text.replace(",", "")
                    if n == "报表日期":
                        o = v
                        continue
                    if v:
                        result.append((n, v, o))
        except requests.Timeout:
            traceback.print_exc()
        return result

    def get_cashflow(self, code: str):
        result = []
        url = "http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/part/displaytype/4.phtml".format(
            code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find(id="ProfitStatementNewTable0")
            o = ""
            if table:
                for tr in table.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) <= 1:
                        continue
                    n = tds[0].text
                    v = tds[1].text.replace(",", "")
                    if n == "报表日期":
                        o = v
                        continue
                    if v:
                        result.append((n, v, o))
        except requests.Timeout:
            traceback.print_exc()
        return result

    def get_profit(self, code: str):
        result = []
        url = "http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{" \
              "}/ctrl/part/displaytype/4.phtml".format(code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find(id="ProfitStatementNewTable0")
            o = ""
            if table:
                for tr in table.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) <= 1:
                        continue
                    n = tds[0].text
                    v = tds[1].text.replace(",", "")
                    if n == "报表日期":
                        o = v
                        continue
                    if v:
                        result.append((n, v, o))
        except requests.Timeout:
            traceback.print_exc()
        return result

    def get_summary(self, code: str):
        result = []
        url = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/{}/displaytype/4.phtml".format(
            code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find(id="FundHoldSharesTable")
            o = ""
            if table:
                for tr in table.find_all("tr"):
                    tds = tr.find_all("td")
                    if len(tds) <= 1:
                        continue
                    n = tds[0].text
                    v = tds[1].text.replace(",", "")
                    if n == "截止日期":
                        if o:
                            break
                        else:
                            o = v
                        continue
                    if v and n:
                        v = v.replace("元", "") if "元" in v else "--"
                        result.append((n, v, o))
        except requests.Timeout:
            traceback.print_exc()
        return result


if __name__ == '__main__':
    job = SinaInfo()
    print(job.get_summary("600597"))
