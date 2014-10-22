import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

class CommentPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Leave Comments Here")
