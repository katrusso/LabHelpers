import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import labpages
import meow
import comment
"""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
"""


MAIN_PAGE_FOOTER_TEMPLATE = """\
<html>
  <body>
    <div align="right">
      <form action="/comment" method="link">
        <div><input type="submit" value="Comment"></div>
      </form>
    </div>
    <br>
    <a href="/StaticLab/1"> Lab 1 </a> &nbsp &nbsp &nbsp <a href="/DynamicLab/1"> Practice Problems for Lab 1 </a> <br>
    <a href="/StaticLab/2"> Lab 2 </a> <br>
    <div align="right">
      <form action="/meow" method="link">
        <div><input type="submit" value="Meow"></div>
      </form>
    </div>
  </body>
</html>
"""

class MyPage(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        if user:
           self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        else:
            self.redirect(users.create_login_url(self.request.uri))

#List of all pages for the application
application = webapp2.WSGIApplication([
    ('/', MyPage),
    ('/StaticLab/1', labpages.StaticLabPage),
    ('/DynamicLab/1', labpages.DynamicLabPage),
    ('/StaticLab/2', labpages.StaticLabPage),
    ('/meow', meow.MeowPage),
    ('/comment', comment.CommentPage),
], debug=True)
