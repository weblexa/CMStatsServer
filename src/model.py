from base import BaseShardedCounter
from google.appengine.ext import db
from google.appengine.api import memcache
from utils import parseModVersion, MemcacheObject
import logging

def query_counter(q, cursor=None, limit=500):
    if cursor:
        q.with_cursor(cursor)
    count = q.count(limit=limit)
    if count == limit:
        return count + query_counter(q, q.cursor(), limit=limit)
    return count

class Device(db.Model):
    type = db.StringProperty()
    version = db.StringProperty()
    version_raw = db.StringProperty()
    country_code = db.StringProperty()
    carrier = db.StringProperty()
    first_seen = db.DateTimeProperty(auto_now_add=True)
    last_seen = db.DateTimeProperty(auto_now=True)

    @classmethod
    def getCount(cls):
        mo = MemcacheObject("Device.getCount")
        if mo.get() is None:
            total = query_counter(cls.all())            
            return mo.set(total, 1)
        else:
            return mo.get()

    def updateCarrier(self, carrier):
        rollback = False
        if carrier == "T - Mobile":
            carrier = "T-Mobile"

        if not self.carrier and carrier:
            s = DeviceCarriers.increment(carrier)
            if s is None:
                rollback = True
            self.carrier = carrier

        return rollback

    def updateCountry(self, country):
        rollback = False
        if not self.country_code and country != "Unknown" and country:
            s = DeviceCountries.increment(country)
            if s is None:
                rollback = True
            self.country_code = country

        return rollback

    def updateVersion(self, version_raw):
        rollback = False
        version_clean = parseModVersion(version_raw)

        if not self.version:
            s = DeviceVersions.increment(version_clean)
            if s is None:
                rollback = True

        if not self.version_raw and version_clean == "Unknown":
            s = UnknownVersions.increment(version_raw)
            if s is None:
                rollback = True

        # This looks like an upgrade, decrement the previous version.
        if self.version and self.version != version_clean:
            s = DeviceVersions.decrement(self.version)
            if s is None:
                rollback = True
            s = DeviceVersions.increment(version_clean)
            if s is None:
                rollback = True

        if self.version == "Unknown" and self.version_raw and self.version_raw != version_raw:
            s = UnknownVersions.decrement(self.version_raw)
            if s is None:
                rollback = True
            s = UnknownVersions.increment(version_raw)
            if s is None:
                rollback = True

        # Finally, update the versions.
        self.version = version_clean
        self.version_raw = version_raw

        return rollback

    @classmethod
    def add(cls, **kwargs):
        rollback = False
        device = cls.get_by_key_name(kwargs.get('key_name'))

        # Sanity Checks
        if kwargs.get('key_name') is None:
            return
        if kwargs.get('device') is None:
            logging.debug("Device is none, returning.")
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
            s = DeviceAggregate.increment(device.type)
            if s is None:
                rollback = True

        if device.updateCarrier(kwargs.get('carrier')) is True:
            logging.debug("updateCarrier is rolling back.")
            rollback = True
        if device.updateCountry(kwargs.get('country')) is True:
            logging.debug("updateCountry is rolling back.")
            rollback = True
        if device.updateVersion(kwargs.get('version')) is True:
            logging.debug("updateVersion is rolling back.")
            rollback = True

        if not rollback:
            device.put()
        else:
            logging.debug("Rolling back.")

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
