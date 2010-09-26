import re
from google.appengine.api import memcache
import logging

def parseModVersion(modver):
    match = re.match(r"^CyanogenMod-(.*)-.*$", modver)
    if match:
        version = match.groups()[0]
        if "NIGHTLY" in version:
            version = "Nightly"
    else:
        version = "Unknown"

    return version

class MemcacheObject(object):
    def __init__(self, key):
        key = "0_%s" % key
        self.key = key
        self.value = memcache.get(key)

    def set(self, value, expiration=1):
        logging.debug("MemcacheObject(%s) e:%s v:%s" % (self.key, expiration, value))
        memcache.add(self.key, value, expiration)
        self.value = value
        return self.get()

    def get(self):
        return self.value

if __name__ == '__main__':
    mo = MemcacheObject('key')
    print mo
