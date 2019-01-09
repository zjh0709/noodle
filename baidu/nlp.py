from aip import AipNlp
from baidu.config import API_KEY, APP_ID, SECRET_KEY
import re


class Nlp(object):

    def __init__(self):
        self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        self.filter_patten = re.compile(u"[^a-zA-Z\u4e00-\u9fa5\s]+")

    def keyword(self, title: str, content: str):
        content = self.filter_patten.sub("", content)
        result = self.client.keyword(title, content)
        return [d.get("tag") for d in result.get("items", []) if "tag" in d]


if __name__ == '__main__':
    title_ = "[振东制药]微商售食药不能没门槛"
    content_ = """
微商交易已经形成一定规模,由于没有明确的法律法规约束,行业“野蛮生长”态势明显,法律缺位纵容了不法分子明目张胆销售假冒伪劣食品药品,监管部门只能事后监管,治本很难。从微信朋友圈里买衣服、面膜、减肥药,已成为不少人的消费习惯。同时,在网络直播节目中推销各种消费品的行为,也已屡见不鲜。据腾讯数据显示,微信月活用户量超过8亿。中国互联网协会微商工作组统计数据显示,2016年,微商行业总体市场规模已超过3600亿元,全国微商从业者高达1535万人,持续呈高速增长态势。中国互联网协会微商工作组秘书长于立娟坦言:“微商交易已经形成了一定规模,由于没有明确的法律法规约束,行业‘野蛮生长’态势较为明显。调查发现,微商从业者大多文化层次不高,甚至对法律知识一无所知,再加上社交的私密属性和闭环特点,微商出现了制假售假、虚假宣传等问题。”来自中国消费者协会的数据显示:2016年,中国网络消费不满意率排行中,微商以5.6%的比例居首位,由于监管缺失,消费者维权无门,卖家销售假货的机会成本较低,造成目前微商市场“三无”产品泛滥、价格虚高、无法维权等怪现象难以遏制。与其他假劣商品相比,假劣食品、药品很可能对公众健康产生直接危害,已引起监管部门的高度重视。根据近年来对网售食品药品违法犯罪行为的监测、打击经验,北京市食品药品稽查总队网监大队队长李�G认为,犯罪嫌疑人在知晓其所售商品为假药或有毒有害食品的情况下,为逃避打击,会在网店网页上采取隐藏式宣传方式,一般不直接在网页上宣传违法产品,而是通过微信、QQ等网络通讯工具与客户沟通,达成意向后再以购买其他产品的名义付款交易。此外,由于微商兜售的商品、信息只通过“朋友圈”这样的社交平台传播,当商品出现质量问题时,也很容易在熟人关系间被“消化”掉。“即使收到举报,对于涉及微商的案件,以现在的行政手段,调查取证难度也极大。”李�G说。更大的挑战在于,对于微商平台性质和责任的认定。新版《食品安全法》对网售食品增设了责任条款,其中要求网络食品交易第三方平台要对入网经营者实名登记,明确其食品安全管理责任。不过,中国电子商务协会政策法律委员会副主任阿拉木斯指出,现行《食品安全法》有利于规范微商的食品销售行为,至于微商是否有法必依,监管部门是否能够做到违法必究,还有很多难题需要破解。比如,平台到底应该承担怎样的社会责任和法律责任,还需进一步明确,大量微商没有遵循基本法律要求,“零门槛”进入网络社交平台,并在其上大量销售各类真假难辨的食品药品,平台应该如何加以约束等。“互联网发展催生了很多新业态,微商就是一个典型。近年来,微商呈现蓬勃发展之势,这种趋势已经很难逆转。但从行业发展来看,微商销售的‘三无’产品潜在危害非常大,完全有必要将微商纳入互联网食品药品监管的序列,既要对交易主体严格审查,互联网平台也要承担相关的责任。”中国营养保健食品协会秘书长刘学聪建言。然而,对于微商是不是“电商”,是否应与淘宝、天猫、京东等电商平台纳入一视同仁地监管,目前尚缺乏专门的法律适用条款。李�G认为,法律的缺位纵容了不法分子在微信朋友圈明目张胆地销售假冒伪劣食品药品,相关监管部门,只能事后监管,很难达到治本的作用,“应该由微信平台制定相关规则,比如审核商家销售资质,这样才会遏制住微商乱象”。中国人民大学食品安全治理协同创新中心研究员肖平辉认为,互联网食品药品交易中涉及两个关键功能,一个是互联网信息功能,一个就是交易功能,互联网交易的监管要牵住这两个牛鼻子,除了从源头治理,抓生产环节,还应该把平台治理作为一个重要的抓手,要让平台担起责任,如此才能对打着“微商”幌子销售伪劣产品的不法行为产生约束。鉴于行业法律规范的有限性,专家建议,最好借助正在立法进程中的《电子商务法》,从市场准入、权利义务、机制保障、监督管理等方面对微商这一电子商务时代的新业态实行全面监管,促进其逐步走上规范运行之路。  
    """
    print(title_)
    # print(Nlp().keyword(title_, content_))
