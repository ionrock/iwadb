from multiprocessing import Process

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

from iwadb import config
from iwadb.db import getdb
from iwadb.message import IWAMessage


class WriterProcess(Process):

    def __init__(self, kafka_host=None):
        self.kafka_host = kafka_host or config.KAFKA_HOST
        super(WriterProcess, self).__init__()

    def run(self):
        env = getdb()
        client = KafkaClient(self.kafka_host)
        consumer = SimpleConsumer(client,
                                  config.KAFKA_GROUP_ID,
                                  config.KAFKA_TOPIC)

        for resp in consumer:
            if not resp.message.value:
                continue

            with env.begin(write=True) as txn:
                message = IWAMessage.loads(resp.message.value)
                print(message)
                txn.put(message.key, message.value)
