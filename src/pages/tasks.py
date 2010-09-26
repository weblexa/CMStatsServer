from base import BasePage
from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from model import DeviceAggregate, Device, DeviceCarriers, DeviceVersions, \
    DeviceCountries, UnknownVersions
import logging
import random

class AggregateDevicesPage(BasePage):
    def get(self):
        for row in DeviceAggregate.all():
            row.delete()

        total = (Device.all().count() / 10)
        for x in xrange(total):
            offset = x * 10
            taskqueue.add(url='/tasks/AggregateDevicesWorker', params={'offset': offset})

class AggregateDevicesWorkerPage(BasePage):
    def post(self):
        offset = int(self.request.get('offset'))

        devices = Device.all().fetch(10, offset) + 1
        for device in devices:
            logging.debug("Device: %s" % device.key().name())
            DeviceAggregate.increment(device.type)

class AggregateCarriersPage(BasePage):
    def get(self):
        for row in DeviceCarriers.all():
            row.delete()

        total = (Device.all().count() / 10) + 1
        for x in xrange(total):
            offset = x * 10
            taskqueue.add(url='/tasks/AggregateCarriersWorker', params={'offset': offset})

class AggregateCarriersWorkerPage(BasePage):
    def post(self):
        offset = int(self.request.get('offset'))

        devices = Device.all().fetch(10, offset)
        for device in devices:
            logging.debug("Device: %s" % device.key().name())
            if not device.carrier:
                device.carrier = "Unknown"
            DeviceCarriers.increment(device.carrier)

class AggregateVersionsPage(BasePage):
    def get(self):
        for row in DeviceVersions.all():
            row.delete()

        total = (Device.all().count() / 10) + 1
        for x in xrange(total):
            offset = x * 10
            taskqueue.add(url='/tasks/AggregateVersionsWorker', params={'offset': offset})

class AggregateVersionsWorkerPage(BasePage):
    def post(self):
        offset = int(self.request.get('offset'))

        devices = Device.all().fetch(10, offset)
        for device in devices:
            logging.debug("Device: %s" % device.key().name())
            DeviceVersions.increment(device.version)

class AggregateCountriesPage(BasePage):
    def get(self):
        for row in DeviceCountries.all():
            row.delete()

        total = (Device.all().count() / 10) + 1
        for x in xrange(total):
            offset = x * 10
            taskqueue.add(url='/tasks/AggregateCountriesWorker', params={'offset': offset})

class AggregateCountriesWorkerPage(BasePage):
    def post(self):
        offset = int(self.request.get('offset'))

        devices = Device.all().fetch(10, offset)
        for device in devices:
            logging.debug("Device: %s" % device.key().name())
            if device.country_code:
                DeviceCountries.increment(device.country_code)

class AggregateUnknownVersionsPage(BasePage):
    def get(self):
        for row in UnknownVersions.all():
            row.delete()

        total = (Device.all().filter('version =', 'Unknown').count() / 10) + 1
        for x in xrange(total):
            offset = x * 10
            taskqueue.add(url='/tasks/AggregateUnknownVersionsWorker', params={'offset': offset})

class AggregateUnknownVersionsWorkerPage(BasePage):
    def post(self):
        offset = int(self.request.get('offset'))

        devices = Device.all().filter('version =', 'Unknown').fetch(10, offset)
        for device in devices:
            logging.debug("Device: %s" % device.key().name())
            if device.version_raw:
                UnknownVersions.increment(device.version_raw)

application = webapp.WSGIApplication(
        [
            ('/tasks/AggregateDevices', AggregateDevicesPage),
            ('/tasks/AggregateDevicesWorker', AggregateDevicesWorkerPage),
            ('/tasks/AggregateCarriers', AggregateCarriersPage),
            ('/tasks/AggregateCarriersWorker', AggregateCarriersWorkerPage),
            ('/tasks/AggregateVersions', AggregateVersionsPage),
            ('/tasks/AggregateVersionsWorker', AggregateVersionsWorkerPage),
            ('/tasks/AggregateCountries', AggregateCountriesPage),
            ('/tasks/AggregateCountriesWorker', AggregateCountriesWorkerPage),
            ('/tasks/AggregateUnknownVersions', AggregateUnknownVersionsPage),
            ('/tasks/AggregateUnknownVersionsWorker', AggregateUnknownVersionsWorkerPage),
        ],
         debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
