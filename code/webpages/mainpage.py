import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

#Other webpage files
import comment
import labpages
import meow
import userpage
import admin
import addquestion
import addtopic
import addlab
import userclass


from html_constants import *

#main page that is initially run
class MainPage(webapp2.RequestHandler):
    def get(self):
        
        username = users.get_current_user()
        if username:
            user_object = userclass.sign_in(self,username.nickname())
            #include the css sheets and open the html
            self.response.write(OPEN_HTML.substitute(head='''<link type="
            text/css" rel="stylesheet" href="/stylesheets/home.css" 
                />'''))
            
            self.response.write(CSS_HTML.substitute(id="header"))
            self.response.write(ALIGN_HTML.substitute(align="center"))
            self.response.write("<h1>LabHelpers</h1>")
            self.response.write(CLOSE_ALIGN_HTML)
            self.response.write(CLOSE_CSS_HTML)#header

            self.response.write(CSS_HTML.substitute(id="nav"))
            self.response.write("<br>")
            self.response.write(ALIGN_HTML.substitute(align="center"))
            self.response.write("<br>")
            if users.is_current_user_admin(): 
                self.response.write(LINK_HTML.substitute(link="/admin", text="Admin Page"))
            self.response.write("<br>")
            self.response.write(LINK_HTML.substitute(link="/comment", text="Comment"))
            self.response.write("<br>")
            self.response.write(LINK_HTML.substitute(link="/meow", text="Meow"))
            self.response.write("<br>")
            self.response.write(CLOSE_ALIGN_HTML)
            self.response.write(CLOSE_CSS_HTML)#nav
            #self.response.write("<br><br>")

            self.response.write(CSS_HTML.substitute(id="content"))
            self.response.write("<br>")
            self.response.write(ALIGN_HTML.substitute(align="center"))
            self.response.write(LINK_HTML.substitute(link="/StaticLab/17/",
                                                     text="Lab 17:Exam 2 Review"))
            self.response.write("<br>")
            self.response.write(CLOSE_ALIGN_HTML)
            self.response.write(CLOSE_CSS_HTML)#content
            
            self.response.write(CSS_HTML.substitute(id="footer"))
            self.response.write("<br>")
            self.response.write(TAB_HTML)
            self.response.write("Content from Physics II Laboratory Manual by Scott Dwyer<br>")
            self.response.write(TAB_HTML)
            self.response.write("Team members: Gerrett Diamond, Seungyeon Lee, Kat Russo, Nick Stamm")
            self.response.write("</div>")#footer
            
                
        # If user is not logged in redirect to log in
        else:
            self.redirect(users.create_login_url(self.request.uri))
    def post(self):
        self.redirect(users.create_login_url(self.request.uri))
#List of all pages for the application
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', userpage.SignUp),
    ('/StaticLab/17/', labpages.StaticLabPage),
    ('/DynamicLab/17/', labpages.DynamicLabPage),
    ('/meow', meow.MeowPage),
    ('/comment', comment.CommentPage),
    ('/sign', comment.Comment),
    ('/admin', admin.Admin),
    ('/admin/questions', addquestion.AddQuestion),
    ('/admin/topic', addtopic.AddTopic),
    ('/admin/lab', addlab.AddLab),
], debug=True)
