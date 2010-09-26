from base import BasePage
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import DeviceCarriers
import re
from django.utils import simplejson

class CarrierPage(BasePage):
    def json(self):
        json = simplejson.dumps(DeviceCarriers.generateGraphData())
        self.response.out.write(json)

    def html(self):
        self.render({
            'carrier_data_len': len(DeviceCarriers.generateGraphData()),
            'carrier_data': DeviceCarriers.generateGraphData()
        })

    def get(self):
        match = re.match(r"^/data/carriers\.(json|html)$", self.request.path)
        if match:
            if match.groups()[0] == 'json':
                self.json()
            elif match.groups()[0] == 'html':
                self.html()
        else:
            self.html()

application = webapp.WSGIApplication(
        [('/data/carriers.*', CarrierPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
