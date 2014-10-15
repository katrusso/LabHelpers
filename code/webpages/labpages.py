import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import labpages
"""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
"""

class StaticLabPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('meow<br>')
        self.response.write(self.request.uri)

class DynamicLabPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('dynamic meow<br>')
        self.response.write(self.request.uri)
