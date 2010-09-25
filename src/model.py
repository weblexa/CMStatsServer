from google.appengine.ext import db
from utils import parseModVersion
import logging

DEVICES = ['bravo','dream_sapphire', 'espresso', 'hero', 
           'heroc', 'inc', 'liberty', 'passion', 'sholes', 'supersonic']

class Device(db.Model):
    type = db.StringProperty()
    version = db.StringProperty()
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
        
        device = cls.get_by_key_name(key_name)
        logging.debug("/submit device = %s" % device)
        if device is None:
            device = cls(key_name=key_name)
            DeviceAggregate.increment(device_type)
            
        device.type = device_type
        device.version = device_version
        device.put()

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
    def generateGraph(cls):
        url = "http://chart.apis.google.com/chart?chs=600x225&cht=p&chco=01A0A3&chd=t:%(values)s&chdl=%(devices)s&chl=%(devices)s&chtt=Installations+by+Device"
        
        counts = cls.all().fetch(100)
        values = {}
        for device in counts:
            values[device.type] = device.count
            
        values = {
            'values': ",".join([str(x) for x in values.values()]),
            'devices': "|".join(values.keys())          
        }
        
        url = url % values
        
        return url