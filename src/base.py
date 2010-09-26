from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from utils import MemcacheObject
import os

class BasePage(webapp.RequestHandler):
    def __init__(self):
        self.tpl_base = os.path.join(os.path.dirname(__file__), 'templates')

    def render(self, values={}):
        cls = self.__class__.__name__
        tpl = os.path.join(self.tpl_base, "%s.html" % (cls))
        self.response.out.write(template.render(tpl, values))

class BaseCounter(db.Model):
    count = db.IntegerProperty()

    @classmethod
    def increment(cls, key):
        counter = cls.get_by_key_name(key)
        if counter is None:
            counter = cls(key_name=key)
            counter.count = 0

        counter.count += 1
        counter.put()

    @classmethod
    def decrement(cls, key):
        counter = cls.get_by_key_name(key)
        if counter is None:
            counter = cls(key_name=key)
            counter.count = 0

        counter.count -= 1
        counter.put()

    @classmethod
    def generateGraphData(cls):
        mo = MemcacheObject("%s.generateGraphData" % cls.__name__)
        if mo.get() is None:
            query = cls.all().fetch(1000)
            values = []
            for row in query:
                value = (row.key().name(), row.count)
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()
