from quartz.Quartz import Quartz
from script import model_script


class ModelQuartz(Quartz):

    def config(self):
        self.schedudler.add_job(model_script.clear_keyword, "cron", hour="*/1", minute="21, 51")
        self.schedudler.add_job(model_script.reset_keyword, "cron", hour="*/1", minute="22, 52")
        self.schedudler.add_job(model_script.run_keyword, "cron", hour="*/1", minute="25, 55")


if __name__ == '__main__':
    ModelQuartz().start()
