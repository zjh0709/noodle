import traceback

import requests
from bs4 import BeautifulSoup

from spider.website import WebSite


class HexunInfo(WebSite):

    def __init__(self):
        self.domain = "hexun"
        self.category = "info"
        super().__init__()

    def get_info(self, code: str):
        info = {}
        url = "http://stockdata.stock.hexun.com/gszl/s{}.shtml".format(code)
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            r.encoding = "gbk"
            soup = BeautifulSoup(r.text, "html.parser")
            for tr in soup.find_all("tr"):
                td = tr.find_all("td")
                if td and len(td) == 2:
                    info.setdefault(td[0].text.strip(), td[1].text.strip())
        except TypeError:
            traceback.print_exc()
        except requests.Timeout:
            traceback.print_exc()
        result = []
        result.append(("名称", info["公司简称"], "")) if "公司简称" in info else None
        result.append(("全称", info["公司全称"], "")) if "公司全称" in info else None
        result.append(("英文名称", info["公司英文名称"], "")) if "公司英文名称" in info else None
        for v in info["曾用名"].split("、") if "曾用名" in info else []:
            result.append(("曾用名", v, ""))
        result.append(("成立日期", info["成立日期"], "")) if "成立日期" in info else None
        for v in info["所属行业"].split("、") if "所属行业" in info else []:
            result.append(("行业", v, ""))
        for v in info["所属概念"].split("、") if "所属概念" in info else []:
            result.append(("概念", v, ""))
        result.append(("地域", info["所属地域"], "")) if "所属地域" in info else None
        result.append(("法定代表人", info["法定代表人"], "")) if "法定代表人" in info else None
        for v in info["独立董事"].split("、") if "独立董事" in info else []:
            result.append(("独立董事", v, ""))
        result.append(("咨询服务机构", info["咨询服务机构"], "")) if "咨询服务机构" in info else None
        result.append(("会计师事务所", info["会计师事务所"], "")) if "会计师事务所" in info else None
        result.append(("证券事务代表", info["证券事务代表"], "")) if "证券事务代表" in info else None
        result.append(("注册资本", info["注册资本"].replace(",", ""), "")) if "注册资本" in info else None
        result.append(("注册地址", info["注册地址"], "")) if "注册地址" in info else None
        result.append(("办公地址", info["办公地址"], "")) if "办公地址" in info else None
        for v in info["主要产品(业务)"].split("、") if "主要产品(业务)" in info else []:
            result.append(("产品", v, ""))
        result.append(("发行日期", info["发行日期"], "")) if "发行日期" in info else None
        result.append(("上市日期", info["上市日期"], "")) if "上市日期" in info else None
        result.append(("上市交易所", info["上市交易所"], "")) if "上市交易所" in info else None
        result.append(("证券类型", info["证券类型"], "")) if "证券类型" in info else None
        result.append(("流通股本", info["流通股本"].replace(",", ""), "")) if "流通股本" in info else None
        result.append(("主承销商", info["主承销商"], "")) if "主承销商" in info else None
        result.append(("发行价", info["发行价"], "")) if "发行价" in info else None
        result.append(("上市首日开盘价", info["上市首日开盘价"], "")) if "上市首日开盘价" in info else None
        result.append(("上市首日涨跌幅", info["上市首日涨跌幅"], "")) if "上市首日涨跌幅" in info else None
        result.append(("上市首日换手率", info["上市首日换手率"], "")) if "上市首日换手率" in info else None
        result.append(("特别处理和退市", info["特别处理和退市"], "")) if "特别处理和退市" in info else None
        result.append(("发行市盈率", info["发行市盈率"], "")) if "发行市盈率" in info else None
        result.append(("公司网址", info["公司网址"], "")) if "公司网址" in info else None
        result.append(("联系人", info["联系人"], "")) if "联系人" in info else None
        return result


if __name__ == '__main__':
    job = HexunInfo()
    print(job.get_info("600690"))
