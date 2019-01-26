from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time

schedudler = BlockingScheduler()


@schedudler.scheduled_job("interval", seconds=3)
def f():
    print("{} hello A".format(datetime.datetime.now()))
    time.sleep(30)
    print("A complete")


@schedudler.scheduled_job("interval", seconds=5)
def g():
    print("{} hello B".format(datetime.datetime.now()))
    time.sleep(30)
    print("B complete")


if __name__ == '__main__':
    schedudler.start()
