import logging
import json

import cherrypy
import lmdb

from multiprocessing import Process

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
from kafka.consumer import SimpleConsumer


def getdb(path=None):
    return lmdb.open(path or 'db.lmdb')


class DBApp(object):

    exposed = True

    def __init__(self, db=None):
        self.db = db or getdb()

    def GET(self, *key):
        key = '/'.join(key)
        with self.db.begin() as txn:
            return txn.get(key)

    def PUT(self, *key):
        key = '/'.join(key)
        cherrypy.engine.publish('dbwrite', key, cherrypy.request.body.read())
        return cherrypy.request.body


class KafkaClientPlugin(cherrypy.process.plugins.SimplePlugin):

    def start(self):
        self.client = KafkaClient('localhost:9092')
        self.producer = SimpleProducer(self.client)
        self.writer = WriterProcess()
        self.writer.start()
        self.bus.subscribe('dbwrite', self.dbwrite)

    def stop(self):
        self.writer.terminate()
        self.client.close()

    def dbwrite(self, key, value):
        self.producer.send_messages('db-writes', json.dumps({key: value}))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    config = {'/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }}

    cherrypy.tree.mount(DBApp(), '/', config)
    cherrypy.engine.kafka = KafkaClientPlugin(cherrypy.engine)
    cherrypy.engine.kafka.subscribe()

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
