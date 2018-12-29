from collections import namedtuple


Article = namedtuple("Article", "domain url code title content date org author classify category")
Article.__new__.__defaults__ = ("", "", "", "", "", "", "", "", "", "", "")
Page = namedtuple("Page", "domain url code category")
Page.__new__.__defaults__ = ("", "", "", "")