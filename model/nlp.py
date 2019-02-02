import re


class Nlp(object):

    model_name = ""
    filter_patten = re.compile(u"[^a-zA-Z\u4e00-\u9fa5\s]+")

    def __init__(self):
        pass

    def keyword(self, title: str, content: str) -> list:
        pass

