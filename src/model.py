from google.appengine.ext import db
from utils import parseModVersion, getGeoIPCode, MemcacheObject
import logging

DEVICES = ['bravo', 'dream_sapphire', 'espresso', 'hero',
           'heroc', 'inc', 'liberty', 'passion', 'sholes', 'supersonic']

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
            return mo.set(devices, 30)
        else:
            return mo.get()

    def updateCarrier(self, carrier):
        # Increment the counter if the carrier was not previously defined.
        if not self.carrier and carrier:
            DeviceCarriers.increment(carrier)
            self.carrier = carrier

    def updateCountry(self, country, ip):
        # Increment the country if it was not previously defined.
        if country is None or country is "Unknown":
            if not self.country_code:
                country = getGeoIPCode(ip)

        if not self.country_code or self.country_code == "Unknown":
            self.country_code = country
            DeviceCountries.increment(country)

    def updateVersion(self, raw_version):
        raw_version = "CyanogenMod-6.1.0-RC0-N1"
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
        device.updateCountry(kwargs.get('country'), kwargs.get('ip'))
        device.updateVersion(kwargs.get('version'))
        device.put()

class DeviceCarriers(db.Model):
    carrier = db.StringProperty()
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, carrier):
        counter = cls.get_by_key_name(carrier)
        if counter is None:
            counter = cls(key_name=carrier)
            counter.carrier = carrier
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def decrement(cls, carrier):
        counter = cls.get_by_key_name(carrier)
        if counter is None:
            counter = cls(key_name=carrier)
            counter.carrier = carrier
            counter.count = 0

        counter.count -= 1
        counter.put()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("DeviceCarriers.generateGraphData")
        if mo.get() is None:
            counts = cls.all().fetch(100)
            values = []
            for carrier in counts:
                value = (carrier.carrier, carrier.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()

class DeviceVersions(db.Model):
    version = db.StringProperty()
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, version):
        counter = cls.get_by_key_name(version)
        if counter is None:
            counter = cls(key_name=version)
            counter.version = version
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def decrement(cls, version):
        counter = cls.get_by_key_name(version)
        if counter is None:
            counter = cls(key_name=version)
            counter.version = version
            counter.count = 0

        counter.count -= 1
        counter.put()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("DeviceVersions.generateGraphData")
        if mo.get() is None:
            counts = cls.all().fetch(100)
            values = []
            for version in counts:
                value = (version.version, version.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()

class DeviceCountries(db.Model):
    country_code = db.StringProperty()
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, country_code):
        counter = cls.get_by_key_name(country_code)
        if counter is None:
            counter = cls(key_name=country_code)
            counter.country_code = country_code
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("DeviceCountries.generateGraphData")
        if mo.get() is None:
            counts = cls.all().fetch(1000)
            values = []
            for device in counts:
                value = (device.country_code, device.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()

class DeviceAggregate(db.Model):
    type = db.StringProperty()
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, device):
        counter = cls.get_by_key_name(device)
        if counter is None:
            counter = cls(key_name=device)
            counter.type = device
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def getCount(cls):
        mo = MemcacheObject("DeviceAggregate.getCount")
        if mo.get() is None:
            devices = db.GqlQuery("SELECT * FROM DeviceAggregate").count()
            return mo.set(devices)
        else:
            return mo.get()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("DeviceAggregate.generateGraphData")
        if mo.get() is None:
            counts = cls.all().fetch(100)
            values = []
            for device in counts:
                value = (device.type, device.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()

class UnknownVersions(db.Model):
    version = db.StringProperty()
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, key):
        counter = cls.get_by_key_name(key)
        if counter is None:
            counter = cls(key_name=key)
            counter.version = key
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def decrement(cls, key):
        counter = cls.get_by_key_name(key)
        if counter is None:
            counter = cls(key_name=key)
            counter.version = key
            counter.count = 0

        counter.count -= 1
        counter.put()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("UnknownVersions.generateGraphData")
        if mo.get() is None:
            counts = cls.all().fetch(100)
            values = []
            for version in counts:
                value = (version.version, version.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()
