from kafka import KafkaConsumer, KafkaProducer
from noodle.common.config import kafka_hosts
import warnings


class KafkaConn(object):
    def __init__(self):
        self.bootstrap_servers = kafka_hosts
        self.topic = None
        self.group_id = None
        self.client_id = None
        self.producer = None
        self.consumer = None

    def set_topic(self, topic: str):
        self.topic = topic
        return self

    def set_group_id(self, group_id: str):
        self.group_id = group_id
        return self

    def set_client_id(self, client_id: str):
        self.client_id = client_id
        return self

    def start(self):
        if self.topic and self.group_id:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                          client_id=self.client_id)
            self.consumer = KafkaConsumer(self.topic,
                                          bootstrap_servers=self.bootstrap_servers,
                                          group_id=self.group_id,
                                          client_id=self.client_id)
            print(self.consumer.config)
        else:
            warnings.warn("topic and group id can't None")

    def stop(self):
        if self.consumer:
            self.consumer.close()
        if self.producer:
            self.producer.close()

    def produce(self, msg: str):
        if self.producer:
            self.producer.send(self.topic, msg.encode())
        else:
            warnings.warn("client not start")

    def consume(self):
        if self.consumer:
            for i in range(10):
                print(next(self.consumer))


if __name__ == '__main__':
    client = KafkaClient()
    client.set_group_id("xjp").set_topic("shanghai").set_client_id("python-client-1")
    client.start()
    # client.consume()
    client.stop()
