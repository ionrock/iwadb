import time
import random
import logging

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

from iwadb.db import getdb
from iwadb.dbwriter import WriterProcess
from iwadb.message import IWAMessage
from iwadb import config


logging.basicConfig(level=logging.INFO)


def random_key():
    chars = 'abcdefghijk1234567890'
    num = random.choice(range(5, 10))
    r = ''.join([random.choice(chars) for x in xrange(num)])
    return r


def run():
    db = getdb()

    writer = WriterProcess()
    writer.start()

    client = KafkaClient(config.KAFKA_HOST)
    producer = SimpleProducer(client)

    timings = []

    for i in range(1000, 2000):
        key = random_key()
        start = time.clock()
        message = IWAMessage(key, i)
        # print('Sending: %s' % message.dumps())
        producer.send_messages(config.KAFKA_TOPIC, message.dumps())
        # print('Queued: %s => %s' % (message.key, message.value))
        while True:
            with db.begin() as txn:
                if txn.get(key):
                    timings.append(time.clock() - start)
                    break

    writer.terminate()

    print('Average write time: %s' % (sum(timings) / len(timings)))
    print('Total write time: %s' % (sum(timings)))


if __name__ == '__main__':
    run()
