"""Our message format."""
import msgpack


class IWAMessage(object):

    def __init__(self, key, value):
        self.key = value
        self.value = value

    def dumps(self):
        msgpack.packb([self.key, self.value], use_bin_type=True)

    @classmethod
    def loads(cls, msg):
        key, value = msgpack.unpackb(msg, encoding='utf-8')
        return cls(key, value)
