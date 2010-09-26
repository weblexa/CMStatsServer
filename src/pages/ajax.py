from base import BasePage
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import Device, DeviceAggregate

class AjaxDeviceCount(BasePage):
    def get(self):
        self.response.out.write("%s" % Device.getCount())

class AjaxDevicesCount(BasePage):
    def get(self):
        self.response.out.write("%s" % DeviceAggregate.getCount())

class LiveCounter(BasePage):
    def get(self):
        self.render({'device_count': Device.getCount()})

application = webapp.WSGIApplication(
        [('/ajax/_Device.getCount', AjaxDeviceCount),
         ('/ajax/_DeviceAggregate.getCount', AjaxDevicesCount),
         ('/ajax/LiveCounter', LiveCounter)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
