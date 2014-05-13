from __future__ import print_function

import logging

import cherrypy

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

from iwadb import config
from iwadb.db import getdb
from iwadb.dbwriter import WriterProcess
from iwadb.message import IWAMessage


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
        cherrypy.engine.publish('dbwrite', key, cherrypy.request.json)
        return cherrypy.request.json


class KafkaClientPlugin(cherrypy.process.plugins.SimplePlugin):

    def start(self):
        self.client = KafkaClient(config.KAFKA_HOST)
        self.producer = SimpleProducer(self.client)
        self.writer = WriterProcess(config.KAFKA_HOST)
        self.writer.start()
        self.bus.subscribe('dbwrite', self.dbwrite)

    def stop(self):
        self.writer.terminate()
        self.client.close()

    def dbwrite(self, key, value):
        message = IWAMessage(key, value)
        self.producer.send_messages(config.KAFKA_TOPIC,
                                    message.dumps())
        cherrypy.log('Queued: %s => %s' % (message.key, message.value))


def run():
    logging.basicConfig(level=logging.DEBUG)

    conf = {'/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.json_in.on': True,
        'tools.json_out.on': True,
    }}

    cherrypy.tree.mount(DBApp(), '/', conf)
    cherrypy.engine.kafka = KafkaClientPlugin(cherrypy.engine)
    cherrypy.engine.kafka.subscribe()

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
