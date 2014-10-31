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
import userclass
import userpage

from html_constants import *

#main page that is initially run
class MainPage(webapp2.RequestHandler):
    def get(self):
        
        username = users.get_current_user()
        if username:
            nickname = username.nickname()
            #check the database for the user
            #if its a new user make the user and push to the database
            user_query = userclass.User.query(
            ancestor=userclass.user_key(nickname)).order(
                userclass.User.rin_number)
            user_object = user_query.fetch()
            if (len(user_object)==0):
                self.redirect("/signup")
            #include the css sheets and open the html
            self.response.write(OPEN_HTML.substitute(head='''<link type="
            text/css" rel="stylesheet" href="/stylesheets/home.css" 
                />'''))
    
                
            #self.response.write('''<div id="main">''')
            #self.response.write("<div>")#main
            
            self.response.write('''<div id="header">''')
            self.response.write(ALIGN_HTML.substitute(align="center"))
            self.response.write("<h1>LabHelpers</h1>")
            self.response.write("</div>")#header

            self.response.write('''<div id="left">''')
            self.response.write("</div>")#left

            self.response.write('''<div id="middle">''')
            self.response.write("<br>")
            self.response.write(TAB_HTML)
            self.response.write(LINK_HTML.substitute(link="/StaticLab/17/",
                                                     text="Lab 17:Exam 2 Review"))
            self.response.write("<br>")
            self.response.write("</div>")#middle
            
            self.response.write('''<div id="right">''')
            self.response.write("<br>")
            self.response.write(ALIGN_HTML.substitute(align="center"))
            if users.is_current_user_admin(): 
                self.response.write(FORM_HTML.substitute(action="/admin",
                                                         method="link"))
                self.response.write(SUBMIT_HTML.substitute(value="Admin Page"))
                self.response.write(CLOSE_FORM_HTML)
            self.response.write(FORM_HTML.substitute(action="/comment",
                                                     method="link"))
            self.response.write(SUBMIT_HTML.substitute(value="Comment"))
            self.response.write(CLOSE_FORM_HTML)
            self.response.write(FORM_HTML.substitute(action="/meow",
                                                     method="link"))
            self.response.write(SUBMIT_HTML.substitute(value="Meow"))
            self.response.write(CLOSE_FORM_HTML)
            self.response.write("</div><br>")
            self.response.write("</div><br>")
            self.response.write("</div>")#right
            
            self.response.write('''<div id="footer">''')
            self.response.write(TAB_HTML)
            self.response.write("<br>Content from Physics II Laboratory Manual by Scott Dwyer")
            self.response.write(TAB_HTML)
            self.response.write("<br>Team members: Gerrett Diamond, Seungyeon Lee, Kat Russo, Nick Stamm")
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
    ('/admin', database.Admin),
    ('/admin/questions', database.AddQuestion),
    ('/admin/topic', database.AddTopic),
], debug=True)
