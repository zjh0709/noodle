from quartz.Quartz import Quartz
from script import spider_script


class SpiderScheduler(Quartz):

    def config(self):
        self.schedudler.add_job(spider_script.reset_topic, "cron", hour="16", minute="08")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="16", minute="09")


if __name__ == '__main__':
    SpiderScheduler().start()
