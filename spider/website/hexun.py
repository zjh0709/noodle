import traceback

import requests
from bs4 import BeautifulSoup

from spider.domain import Domain


class HexunBase(Domain):

    def __init__(self):
        super().__init__()
        self.domain = "hexun"
        self.category = "base"

    def get_info(self, code: str):
        info = {}
        url = "http://stockdata.stock.hexun.com/gszl/s{}.shtml".format(code)
        r = requests.get(url, headers=self.headers)
        r.encoding = "gbk"
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            for tr in soup.find_all("tr"):
                td = tr.find_all("td")
                if td and len(td) == 2:
                    info.setdefault(td[0].text.strip(), td[1].text.strip())
        except TypeError:
            traceback.print_exc()
        if "所属行业" in info:
            info["所属行业"] = info["所属行业"].split("、")
        if "所属概念" in info:
            info["所属概念"] = info["所属概念"].split("、")
        return info


if __name__ == '__main__':
    m = HexunBase()
    print(m.get_info("600597"))
