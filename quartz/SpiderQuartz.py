from quartz.Quartz import Quartz
from script import spider_script


class SpiderScheduler(Quartz):

    def config(self):
        self.schedudler.add_job(spider_script.clear_topic, "cron", hour="*/1", minute="20")
        self.schedudler.add_job(spider_script.reset_topic, "cron", hour="*/1", minute="22")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="25")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="26")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="27")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="28")


if __name__ == '__main__':
    SpiderScheduler().start()
