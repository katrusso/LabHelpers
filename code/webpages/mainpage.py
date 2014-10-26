import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

#Other webpage files
import labpages
import meow
import comment
import database
from html import *
MAIN_PAGE_FOOTER_TEMPLATE = '''\
<html>
  <body>
    <div align="right">
      <form action="" method="post">
        <div><input type="submit" value="Sign Out"></div>
      </form>
      <form action="/comment" method="link">
        <div><input type="submit" value="Comment"></div>
      </form>
    </div>
    <br>
    <a href="/StaticLab/17/"> Lab 17: Exam 2 Review </a> &nbsp &nbsp &nbsp <a href="/DynamicLab/1/"> Practice Problems for Lab 17 </a> <br>
    <div align="right">
      <form action="/meow" method="link">
        <div><input type="submit" value="Meow"></div>
      </form>
    </div>
  </body>
</html>
'''

class MyPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.redirect('/admin')
            else:
                self.response.write(OPEN_HTML.substitute(head=""))
                self.response.write(ALIGN_HTML.substitute(align="right"))
                self.response.write(FORM_HTML.substitute(action="", 
                                                         method="post"))
                self.response.write(SUBMIT_HTML.substitute(value="Sign Out"))
                self.response.write("</form>")
                self.response.write(FORM_HTML.substitute(action="/comment",
                                                         method="link"))
                self.response.write(SUBMIT_HTML.substitute(value="Comment"))
                self.response.write("</form>")
                self.response.write("</div><br>")
                self.response.write(LINK_HTML.substitute(link="/StaticLab/17/",
                                                         text="Lab 17:Exam 2 Review"))
                self.response.write(TAB_HTML)
                self.response.write(LINK_HTML.substitute(link="/DynamicLab/17/",
                                                         text="Practice Problems for Lab 17"))
                self.response.write("<br>")
                self.response.write(ALIGN_HTML.substitute(align="right"))
                self.response.write(FORM_HTML.substitute(action="/meow",
                                                         method="link"))
                self.response.write(SUBMIT_HTML.substitute(value="Meow"))
                self.response.write("</form>")
                self.response.write("<div><br>")
                

        else:
            self.redirect(users.create_login_url(self.request.uri))
        
    #sign out
    def post(self):
        self.redirect(users.create_login_url(self.request.uri))

#List of all pages for the application
application = webapp2.WSGIApplication([
    ('/', MyPage),
    ('/StaticLab/17/', labpages.StaticLabPage),
    ('/DynamicLab/17/', labpages.DynamicLabPage),
    ('/meow', meow.MeowPage),
    ('/comment', comment.CommentPage),
    ('/admin', database.Admin),
    ('/admin/questions', database.AddQuestion),
    ('/admin/topic', database.AddTopic),
], debug=True)
