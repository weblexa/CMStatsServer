from base import BaseShardedCounter
from google.appengine.ext import db
from utils import parseModVersion, MemcacheObject
import logging

class Device(db.Model):
    type = db.StringProperty()
    version = db.StringProperty()
    version_raw = db.StringProperty()
    country_code = db.StringProperty()
    carrier = db.StringProperty()
    first_seen = db.DateTimeProperty(auto_now_add=True)
    last_seen = db.DateTimeProperty(auto_now=True)

    @classmethod
    def getCount(self):
        mo = MemcacheObject("Device.getCount")
        if mo.get() is None:
            devices = db.GqlQuery("SELECT * FROM Device").count()
            return mo.set(devices, 1)
        else:
            return mo.get()

    def updateCarrier(self, carrier):
        if carrier == "T - Mobile":
            carrier = "T-Mobile"

        if not self.carrier and carrier:
            self.carrier = carrier

    def updateCountry(self, country):
        if not self.country_code and country != "Unknown" and country:
            self.country_code = country

    def updateVersion(self, raw_version):
        clean_version = parseModVersion(raw_version)
        self.version = clean_version
        self.version_raw = raw_version

    @classmethod
    def add(cls, **kwargs):
        device = cls.get_by_key_name(kwargs.get('key_name'))

        # Create new record if one does not exist.
        if device is None:
            device = cls(key_name=kwargs.get('key_name'))
            device.type = kwargs.get('type')

        device.updateCarrier(kwargs.get('carrier'))
        device.updateCountry(kwargs.get('country'))
        device.updateVersion(kwargs.get('version'))
        device.put()

class DeviceCarriers(BaseShardedCounter):
    pass

class DeviceVersions(BaseShardedCounter):
    pass

class DeviceCountries(BaseShardedCounter):
    pass

class DeviceAggregate(BaseShardedCounter):
    pass

class UnknownVersions(BaseShardedCounter):
    pass
