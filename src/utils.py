import re
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

if __name__ == '__main__':
    print parseModVersion("CyanogenMod-6-09242010-NIGHTLY-N1")
    print parseModVersion("CyanogenMod-6.0-N1")
    print parseModVersion("CyanogenMod-6.1.0-RC0-Droid")
