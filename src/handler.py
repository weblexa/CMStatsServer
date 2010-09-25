from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from model import Device, DeviceAggregate, DeviceVersions
import logging
import os.path

class MainPage(webapp.RequestHandler):
    def get(self):
        tpl_values = {
            'unique_count': Device.getUniqueCount(),
            'devices_count': DeviceAggregate.getCount(),
            'graph_by_device': DeviceAggregate.generateGraphData(),
            'graph_by_version': DeviceVersions.generateGraphData(),
        }
        
        tpl_path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(tpl_path, tpl_values))

class SubmitPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Invalid Request')
        
    def post(self):
        kwargs = {
            'key_name': self.request.get('id'),
            'type': self.request.get('type'),
            'version': self.request.get('version'),
        }
        Device.update(**kwargs)

application = webapp.WSGIApplication(
        [('/', MainPage), ('/submit', SubmitPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
