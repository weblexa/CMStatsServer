from google.appengine.ext import db
from utils import parseModVersion, getGeoIPCode
import logging

DEVICES = ['bravo','dream_sapphire', 'espresso', 'hero', 
           'heroc', 'inc', 'liberty', 'passion', 'sholes', 'supersonic']

class Device(db.Model):
    type = db.StringProperty()
    version = db.StringProperty()
    version_raw = db.StringProperty()
    country_code = db.StringProperty()
    first_seen = db.DateTimeProperty(auto_now_add=True)
    last_seen = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def getUniqueCount(self):
        devices = db.GqlQuery("SELECT * FROM Device")
        return devices.count()
    
    @classmethod
    def update(cls, **kwargs):
        key_name = kwargs.get('key_name')
        device_type = kwargs.get('type')
        device_version = parseModVersion(kwargs.get('version'))
        device_version_raw = kwargs.get('version')
        
        device = cls.get_by_key_name(key_name)
        logging.debug("/submit device = %s" % device)
        
        # Create new record if one does not exist.
        if device is None:
            device = cls(key_name=key_name)
            DeviceAggregate.increment(device_type)
            DeviceVersions.increment(device_version)
        
        if device.country_code is None:
            country_code = getGeoIPCode(kwargs.get('ip'))
            logging.debug("model country_code = %s" % country_code)
            if country_code:
                DeviceCountries.increment(country_code)
                
        # Update UnknownVersions if necessary.
        if device_version == "Unknown":
            if device.version_raw != device_version_raw:
                UnknownVersions.increment(device_version_raw)
                if device.device_version_raw:
                    UnknownVersions.decrement(device.device_version_raw)
            
        # Update DeviceVersions if necessary.
        if device.version and device.version != device_version:
            DeviceVersions.decrement(device.version)
            DeviceVersions.increment(device_version)
            
        device.type = device_type
        device.version = device_version
        device.version_raw = device_version_raw
        device.country_code = country_code
        device.put()
        
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
        counts = cls.all().fetch(100)
        values = []
        for version in counts:
            value = (version.version, version.count)
            values.append(value)
        
        return values
        
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
        counts = cls.all().fetch(100)
        values = []
        for version in counts:
            value = (version.version, version.count)
            values.append(value)
        
        return values
    
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
        counts = cls.all().fetch(1000)
        values = []
        for device in counts:
            value = (device.country_code, device.count)
            values.append(value)
        
        return values
    
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
        devices = db.GqlQuery("SELECT * FROM DeviceAggregate")
        return devices.count()
    
    @classmethod
    def generateGraphData(cls):
        counts = cls.all().fetch(100)
        values = []
        for device in counts:
            value = (device.type, device.count)
            values.append(value)
        
        return values