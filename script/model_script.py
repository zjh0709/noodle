from model.NlpModel import baidu
from runner.ModelRunner import ModelRunner, logger


def reset_keyword():
    ModelRunner().reset_keyword()


def clear_keyword():
    ModelRunner().clear_keyword()


def run_keyword():
    model_runner = ModelRunner()
    baidu_nlp = baidu.BaiduNlp()
    while True:
        url = model_runner.next_keyword()
        if url is None:
            logger.warning("no url!")
            break
        model_runner.keyword_runner(baidu_nlp, url)


def run_word():
    model_runner = ModelRunner()
    model_runner.save_article_keyword()


if __name__ == '__main__':
    run_keyword()
