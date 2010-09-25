from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import DeviceVersions
import logging

class AggregateVersionsTask(webapp.RequestHandler):
    def get(self):
        DeviceVersions.update()
        self.response.out.write("")

application = webapp.WSGIApplication(
        [('/tasks/aggregate_versions', AggregateVersionsTask)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
