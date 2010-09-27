from google.appengine.api import memcache
import logging

class MemcacheObject(object):
    def __init__(self, key):
        key = "12_%s" % key
        self.key = key
        self.value = memcache.get(key)

    def set(self, value, expiration=30):
        logging.debug("MemcacheObject(%s) e:%s v:%s" % (self.key, expiration, value))
        memcache.add(self.key, value, expiration)
        self.value = value
        return self.get()

    def get(self):
        return self.value

if __name__ == '__main__':
    mo = MemcacheObject('key')
    print mo