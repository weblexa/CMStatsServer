import random
import uuid
import hashlib
import urllib

def getDevice():
    devices = ['espresso','passion','hero','dream','sapphire']
    return devices[random.randrange(0,len(devices))]

def getVersion():
    versions = ['KangMod-v1.0', 'CyanogenMod-6-01012010-NIGHTLY-N1', 'CyanogenMod-6.1.0-N1']
    return versions[random.randrange(0,len(versions))]

def getCarrier():
    return "T-Mobile"

def getCountry():
    return "us"

def getKey():
    return hashlib.md5(str(uuid.uuid4())).hexdigest().upper()

def getURL():
    values = {
        'id': getKey(),
        'type': getDevice(),
        'version': getVersion(),
        'country': getCountry(),
        'carrier': getCarrier()
    }
    url = "http://localhost:8080/submit?%s" % urllib.urlencode(values)
    return url

def main():
    for x in xrange(2000):
        url = getURL()
        urllib.urlopen(url).read()
        print "%i" % x

if __name__ == '__main__':
    main()
