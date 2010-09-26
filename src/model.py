from base import BaseCounter
from google.appengine.ext import db
from utils import parseModVersion, getGeoIPCode, MemcacheObject
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

        # Increment the counter if the carrier was not previously defined.
        if not self.carrier and carrier:
            DeviceCarriers.increment(carrier)
            self.carrier = carrier

    def updateCountry(self, country):
        # Increment the counter if the country was not previously defined.
        if not self.country_code and country != "Unknown" and country:
            DeviceCountries.increment(country)
            self.country_code = country

    def updateVersion(self, raw_version):
        clean_version = parseModVersion(raw_version)

        # Process for a new device.
        if not self.version:
            DeviceVersions.increment(clean_version)
            self.version = clean_version
            self.version_raw = raw_version

            if clean_version == "Unknown":
                UnknownVersions.increment(raw_version)

            return

        # Process for an existing device.
        if self.version and self.version != clean_version:
            DeviceVersions.decrement(self.version)
            DeviceVersions.increment(clean_version)
            self.version = clean_version

        if raw_version == "Unknown":
            if self.version_raw != raw_version:
                UnknownVersions.decrement(self.version_raw)
                UnknownVersions.increment(raw_version)

        self.version_raw = raw_version

    @classmethod
    def add(cls, **kwargs):
        device = cls.get_by_key_name(kwargs.get('key_name'))

        # Create new record if one does not exist.
        if device is None:
            device = cls(key_name=kwargs.get('key_name'))
            DeviceAggregate.increment(kwargs.get('type'))
            device.type = kwargs.get('type')

        device.updateCarrier(kwargs.get('carrier'))
        device.updateCountry(kwargs.get('country'))
        device.updateVersion(kwargs.get('version'))
        device.put()

class DeviceCarriers(BaseCounter):
    pass

class DeviceVersions(BaseCounter):
    pass

class DeviceCountries(BaseCounter):
    pass

class DeviceAggregate(BaseCounter):
    @classmethod
    def getCount(cls):
        mo = MemcacheObject("DeviceAggregate.getCount")
        if mo.get() is None:
            devices = db.GqlQuery("SELECT * FROM DeviceAggregate").count()
            return mo.set(devices)
        else:
            return mo.get()

class UnknownVersions(BaseCounter):
    pass
