from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class BasePage(webapp.RequestHandler):
    def __init__(self):
        self.tpl_base = os.path.join(os.path.dirname(__file__), 'templates')

    def render(self, values):
        cls = self.__class__.__name__
        tpl = os.path.join(self.tpl_base, "%s.html" % (cls))
        self.response.out.write(template.render(tpl, values))
