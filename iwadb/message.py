"""Our message format."""
import json


class IWAMessage(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def dumps(self):
        return json.dumps({'key': self.key, 'value': self.value})

    @classmethod
    def loads(cls, msg):
        try:
            doc = json.loads(msg)
            if isinstance(doc, dict):
                return cls(doc['key'], doc['value'])
        except ValueError:
            print('Error loading: %s' % msg)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.key == other.key and self.value == other.value
