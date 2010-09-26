from base import BaseShardedCounter
from google.appengine.ext import db
from utils import parseModVersion, MemcacheObject

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
            return mo.set(devices, 5)
        else:
            return mo.get()

    def updateCarrier(self, carrier):
        if carrier == "T - Mobile":
            carrier = "T-Mobile"

        if not self.carrier and carrier:
            DeviceCarriers.increment(carrier)
            self.carrier = carrier

    def updateCountry(self, country):
        if not self.country_code and country != "Unknown" and country:
            DeviceCountries.increment(country)
            self.country_code = country

    def updateVersion(self, version_raw):
        version_clean = parseModVersion(version_raw)

        if not self.version:
            DeviceVersions.increment(version_clean)

        if not self.version_raw and version_clean == "Unknown":
            UnknownVersions.increment(version_raw)

        # This looks like an upgrade, decrement the previous version.
        if self.version and self.version != version_clean:
            DeviceVersions.decrement(self.version)
            DeviceVersions.increment(version_clean)

        if self.version == "Unknown" and self.version_raw and self.version_raw != version_raw:
            UnknownVersions.decrement(self.version_raw)
            UnknownVersions.increment(version_raw)

        # Finally, update the versions.
        self.version = version_clean
        self.version_raw = version_raw

    @classmethod
    def add(cls, **kwargs):
        rollback = False
        device = cls.get_by_key_name(kwargs.get('key_name'))

        # Sanity Checks
        if kwargs.get('key_name') is None:
            return
        if kwargs.get('device') is None:
            return
        if kwargs.get('version') is None:
            return
        if kwargs.get('carrier') is None:
            kwargs['carrier'] = "Unknown"
        if kwargs.get('country') is None:
            kwargs['country'] = "Unknown"

        # Create new record if one does not exist.
        if device is None:
            device = cls(key_name=kwargs.get('key_name'))
            device.type = kwargs.get('device')

        if not device.updateCarrier(kwargs.get('carrier')):
            rollback = True
        if not device.updateCountry(kwargs.get('country')):
            rollback = True
        if not device.updateVersion(kwargs.get('version')):
            rollback = True

        if not rollback:
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
