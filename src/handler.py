from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import Device


class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Count: %s' % Device.getUniqueCount())

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
