from quartz.Quartz import Quartz
from script import spider_script


class SpiderScheduler(Quartz):

    def config(self):
        # article
        self.schedudler.add_job(spider_script.clear_topic, "cron", hour="*/1", minute="6,36")
        self.schedudler.add_job(spider_script.reset_topic, "cron", hour="*/1", minute="8,38")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="11,41")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="12,42")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="13,43")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="14,44")

        # topic
        self.schedudler.add_job(spider_script.clear_stock, "cron", hour="0", minute="0")
        self.schedudler.add_job(spider_script.reset_stock, "cron", hour="0", minute="1")
        self.schedudler.add_job(spider_script.run_topic, "cron", hour="0", minute="5")
        self.schedudler.add_job(spider_script.run_topic, "cron", hour="0", minute="6")
        self.schedudler.add_job(spider_script.run_topic, "cron", hour="0", minute="7")
        self.schedudler.add_job(spider_script.run_topic, "cron", hour="0", minute="8")


if __name__ == '__main__':
    SpiderScheduler().start()
