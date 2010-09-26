from base import BasePage
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import Device, DeviceAggregate, DeviceVersions, DeviceCountries, \
    UnknownVersions, DeviceCarriers

class MainPage(BasePage):
    def get(self):
        tpl_values = {
            'device_count': Device.getCount(),
            'devices_count': DeviceAggregate.getCount(),
            'graph_by_device': DeviceAggregate.generateGraphData(),
            'graph_by_version': DeviceVersions.generateGraphData(),
            'graph_by_country': DeviceCountries.generateGraphData(),
            'graph_unknown_versions': UnknownVersions.generateGraphData(),
            'graph_carriers': DeviceCarriers.generateGraphData(),
        }

        self.render(tpl_values)

application = webapp.WSGIApplication(
        [('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
