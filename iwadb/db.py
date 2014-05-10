import lmdb


def getdb(path=None):
    return lmdb.open(path or 'db.lmdb')
