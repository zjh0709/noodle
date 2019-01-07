from aip import AipNlp
from baidu.config import API_KEY, APP_ID, SECRET_KEY


class Nlp(object):

    def __init__(self):
        self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    def keyword(self, title: str, content: str):
        result = self.client.keyword(title, content)
        return [d.get("tag") for d in result.get("items", []) if "tag" in d]


if __name__ == '__main__':
    title_ = "收评：创业板跌1.16% 5G概念大跌军工股强势"
    content_ = """
e公司讯，今日两市低开，早盘军工、券商等板块表现强势，三大股指一度齐翻红，随后冲高回落。午后，沪指窄幅震荡，创业板指持续下行。截至收盘，沪指跌0.04%；深证成指跌0.84%，跌破去年10月份以来低点；创业板指跌1.16%。盘面上，国防军工、黄金、卫星导航、稀土永磁等板块涨幅居前；华为概念、5G概念、次新股、苹果概念、仿制药等跌幅居前。
新浪声明：新浪网登载此文出于传递更多信息之目的，并不意味着赞同其观点或证实其描述。文章内容仅供参考，不构成投资建议。投资者据此操作，风险自担。 
责任编辑：马秋菊 SF186    
    """
    print(Nlp().keyword(title_, content_))
