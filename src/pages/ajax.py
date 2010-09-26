from base import BasePage
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import Device

class AjaxDeviceCount(BasePage):
    def get(self):
        self.response.out.write("%s" % Device.getCount())

class LiveCounter(BasePage):
    def get(self):
        self.render({'device_count': Device.getCount()})

application = webapp.WSGIApplication(
        [('/ajax/_Device.getCount', AjaxDeviceCount),
         ('/ajax/LiveCounter', LiveCounter)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
