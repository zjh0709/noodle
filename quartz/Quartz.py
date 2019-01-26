from apscheduler.schedulers.blocking import BlockingScheduler
from abc import ABCMeta, abstractmethod


class Quartz(metaclass=ABCMeta):

    schedudler = BlockingScheduler()

    def __init__(self):
        self.config()

    @abstractmethod
    def config(self):
        pass

    def start(self):
        self.schedudler.start()


if __name__ == '__main__':
    Quartz().run()
