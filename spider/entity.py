from collections import namedtuple
import copy


Article = namedtuple("Article", "domain url code title content date org author classify category")
Article.__new__.__defaults__ = ("", "", "", "", "", "", "", "", "", "", "")
Page = namedtuple("Page", "domain url code category")
Page.__new__.__defaults__ = ("", "", "", "")


def dict_to_article(article: dict) -> Article:
    article = copy.deepcopy(article)
    for k in set(article.keys()).difference(Article._fields):
        del article[k]
    return Article(**article)


def article_to_dict(article: Article) -> dict:
    return article._asdict()
