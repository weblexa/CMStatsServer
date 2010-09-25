from base import BasePage
from model import Device
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class SubmitPage(BasePage):
    def post(self):
        kwargs = {
            'key_name': self.request.get('id'),
            'type': self.request.get('type'),
            'version': self.request.get('version'),
        }
        Device.update(**kwargs)

application = webapp.WSGIApplication(
        [('/submit', SubmitPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
