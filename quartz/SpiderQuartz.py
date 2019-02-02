from quartz.Quartz import Quartz
from script import spider_script


class SpiderScheduler(Quartz):

    def config(self):
        self.schedudler.add_job(spider_script.clear_topic, "cron", hour="*/1", minute="36")
        self.schedudler.add_job(spider_script.reset_topic, "cron", hour="*/1", minute="38")
        self.schedudler.add_job(spider_script.run_article, "cron", hour="*/1", minute="41-44/1")


if __name__ == '__main__':
    SpiderScheduler().start()
