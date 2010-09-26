from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from utils import MemcacheObject
import hashlib
import logging
import os
import random

class BasePage(webapp.RequestHandler):
    def __init__(self):
        self.tpl_base = os.path.join(os.path.dirname(__file__), 'templates')

    def render(self, values={}):
        cls = self.__class__.__name__
        tpl = os.path.join(self.tpl_base, "%s.html" % (cls))
        self.response.out.write(template.render(tpl, values))

class ShardedCounterRelations(db.Model):
    key_ = db.StringProperty()
    cls_ = db.StringProperty()

class BaseShardedCounter(db.Model):
    SHARDS = 20
    key_ = db.StringProperty()
    count = db.IntegerProperty(required=True, default=0)

    @classmethod
    def decrement(cls, key_):
        # Find a shard to decrement.
        def txn():
            shard = cls.all().filter('count >=', '1').filter('key_ =', key_).get()
            if shard:
                shard.count -= 1
                shard.put()
            return True
        return db.run_in_transaction(txn)

    @classmethod
    def increment(cls, key_):
        # Store unique key.
        cls_key = hashlib.md5(cls.__name__ + "_" + key_).hexdigest()
        relation = ShardedCounterRelations.get_by_key_name(cls_key)
        if relation is None:
            relation = ShardedCounterRelations(key_name=cls_key)
            relation.key_ = key_
            relation.cls_ = cls.__name__
            relation.put()
        def txn():
            # Increment Shard
            idx = random.randint(0, cls.SHARDS - 1)
            shard_name = str(key_) + "_" + str(idx)
            counter = cls.get_by_key_name(shard_name)
            if counter is None:
                counter = cls(key_name=shard_name)
            counter.count += 1
            counter.key_ = key_
            counter.put()
            return True
        return db.run_in_transaction(txn)

    @classmethod
    def getKeyCount(cls):
        relations = ShardedCounterRelations.all() \
                        .filter('cls_ =', cls.__name__) \
                        .count()
        return relations

    @classmethod
    def getCount(cls, key_=None):
        total = 0
        if key_:
            iterator = cls.all().filter('key_ =', key_)
        else:
            iterator = cls.all()
        for counter in iterator:
            total += counter.count
        return total

    @classmethod
    def generateGraphData(cls):
        cls_ = cls.__name__
        mo = MemcacheObject("%s.generateGraphData" % cls.__name__)

        if mo.get() is None:
            keys = ShardedCounterRelations.all().filter('cls_ =', cls_)
            values = []
            for key in keys:
                value = (key.key_, cls.getCount(key.key_))
                values.append(value)

            return mo.set(values)
        else:
            return mo.get()
