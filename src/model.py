from google.appengine.ext import db

class Device(db.Model):
    type = db.StringProperty()
    version = db.IntegerProperty()
    datetime = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def getUniqueCount(self):
        devices = db.GqlQuery("SELECT * FROM Device")
        return devices.count()
    
    @classmethod
    def update(cls, **kwargs):
        device = cls(key_name=kwargs.get('key_name'))
        device.type = kwargs.get('type')
        device.put()
        return device
    
class DeviceTypes(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()