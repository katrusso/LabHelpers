import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

#import bugsnag

#Other webpage files
import comment
import static
import dynamic
import labtopic
import meow
import userpage
import admin
import addquestion
import editquestion
import addtopic
import edittopic
import addlab
import userclass
import lab



from html_constants import *

#main page that is initially run
class MainPage(webapp2.RequestHandler):
    def get(self):
        """
        This method prompts the user to log in via gmail authentication, then loads the 
        main page, including the associated style sheet. 
        
        If the user doesn't have an account, they will be prompted to create one.
        
        Next, navigation links are listed, followed by a section dedicated to labs 
        associated with that particular user.
         
        """
        username = users.get_current_user()
        if username:
            user_object = userclass.sign_in(self,username.nickname())
            
            #homepage stylesheet
            self.response.write(OPEN_HTML.substitute(head='''<link type="   
            text/css" rel="stylesheet" href="/stylesheets/home.css" 
                />'''))
            
            #header
            self.response.write(CSS_HTML.substitute(id="header"))
            self.response.write(ALIGN_HTML.substitute(align="center"))
            self.response.write("<h1>LabHelpers</h1>")
            self.response.write(CLOSE_ALIGN_HTML)
            self.response.write(CLOSE_CSS_HTML)#header

            #navigation links
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

            #lab links
            self.response.write(CSS_HTML.substitute(id="content"))
            self.response.write("<br>")
            self.response.write(ALIGN_HTML.substitute(align="center"))
            lab_query = lab.Lab.query(ancestor=lab.lab_key(1)).order(lab.Lab.id)
            lab_list = lab_query.fetch()
            for lab_object in lab_list:
                self.response.write(LINK_HTML.substitute(
                    link="/StaticLab/"+str(lab_object.id)+"/",
                    text="Lab "+str(lab_object.id)+": "+lab_object.name))
                self.response.write("<br>")
            self.response.write("<br>")
            self.response.write(CLOSE_ALIGN_HTML)
            self.response.write(CLOSE_CSS_HTML)#content
            
            #footer / content sources
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
    ('/StaticLab/.*/', static.StaticLabPage),
    ('/DynamicLab/.*/', dynamic.DynamicLabPage),
    ('/StaticLab/.*/.*', labtopic.LabTopic),
    ('/DynamicLab/.*/.*', labtopic.LabTopic),
    ('/meow', meow.MeowPage),
    ('/comment', comment.CommentPage),
    ('/sign', comment.Comment),
    ('/admin', admin.Admin),
    ('/admin/questions', addquestion.AddQuestion),
    ('/admin/equestions', editquestion.EditQuestion),
    ('/admin/topic', addtopic.AddTopic),
    ('/admin/etopic', edittopic.EditTopic),

    ('/admin/lab', addlab.AddLab),
], debug=True)
