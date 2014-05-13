from iwadb.message import IWAMessage


class TestIWAMessage(object):

    def test_dumps_then_loads(self):
        msg = IWAMessage('foo', 'bar')
        print(msg.dumps())
        assert msg == IWAMessage.loads(msg.dumps())


if __name__ == '__main__':
    tests = [
        TestIWAMessage(),
    ]

    for test in tests:
        for meth in dir(test):
            if meth.startswith('test'):
                getattr(test, meth)()
