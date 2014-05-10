

class WriterProcess(object):

    def __init__(self, kafka_host='localhost:9092'):
        self.kafka_host = kafka_host

    def run(self):
        env = getdb()
        client = KafkaClient(self.kafka_host)
        consumer = SimpleConsumer(client, 'db-workers', 'db-writes')

        for resp in consumer:
            with env.begin(write=True) as txn:
                doc = json.loads(resp.message.value)
                txn.put(doc.keys()[0].encode(), doc.values()[0].encode())
