import re
from google.appengine.api import memcache
from google.appengine.api import urlfetch
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

def getGeoIPCode(ipaddr):
    geoipcode = None
    try:
        fetch_response = urlfetch.fetch('http://geoip.wtanaka.com/cc/%s' % ipaddr)
        if fetch_response.status_code == 200:
            geoipcode = fetch_response.content
    except urlfetch.Error:
        pass

    logging.debug("geoip = %s" % geoipcode)

    return geoipcode

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
