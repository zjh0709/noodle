from quartz.Quartz import Quartz
from script import spider_script


class SpiderScheduler(Quartz):

    def config(self):
        self.schedudler.add_job(spider_script.reset_stock, "cron", hour="*/3")


if __name__ == '__main__':
    SpiderScheduler().start()
