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
from html_constants import *

#main page that is initially run
class MyPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            #if user is admin redirect to admin page
            if users.is_current_user_admin(): 
                self.redirect('/admin')
            #otherwise load mainpage
            else:
                self.response.write(OPEN_HTML.substitute(head='''<link type="text/css" rel="stylesheet" href="/stylesheets/home.css" />'''))
                self.response.write('''<div id="header">''')


                self.response.write('''<div id="left">''')
                self.response.write("</div>")#left


                self.response.write('''<div id="main">''')
                self.response.write("<br>")
                self.response.write(TAB_HTML)
                self.response.write(LINK_HTML.substitute(link="/StaticLab/17/",
                                                         text="Lab 17:Exam 2 Review"))
                self.response.write("<br>")
                self.response.write("</div>")#main


                self.response.write('''<div id="right">''')
                self.response.write("<br>")
                self.response.write(ALIGN_HTML.substitute(align="center"))
                self.response.write(FORM_HTML.substitute(action="", 
                                                         method="post"))
                self.response.write(SUBMIT_HTML.substitute(value="Sign Out"))
                self.response.write("</form>")
                self.response.write(FORM_HTML.substitute(action="/comment",
                                                         method="link"))
                self.response.write(SUBMIT_HTML.substitute(value="Comment"))
                self.response.write("</form>")
                self.response.write(FORM_HTML.substitute(action="/meow",
                                                         method="link"))
                self.response.write(SUBMIT_HTML.substitute(value="Meow"))
                self.response.write("</form>")
                self.response.write("</div><br>")
                self.response.write("</div><br>")
                self.response.write("</div>")#right

                self.response.write("</div>")#header
        # If user is not logged in redirect to log in
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
    ('/sign', comment.Comment),
    ('/admin', database.Admin),
    ('/admin/questions', database.AddQuestion),
    ('/admin/topic', database.AddTopic),
], debug=True)
