import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

#Other webpage files
import userclass

from html_constants import *

#main page that is initially run
class SignUp(webapp2.RequestHandler):
    '''
    THIS IS THE PAGE THE STUDENT FIRST ENCOUNTERS WHEN VISITING THE SITE. IT PROMPTS THEM 
    TO LOG INTO THEIR GMAIL ACCOUNT FOR AUTHENTICATION PURPOSES, THEN ENTER THEIR RIN 
    TO SIGN-UP FOR ACCESS TO THE LABS. FURTHER, IT ACCESS THEIR WORK AT A LATER DATE AS 
    IT IS ASSOCIATED WITH THEIR ACCOUNT DATA. 
    '''
    def __write_submission__(self):
        username = users.get_current_user()                                         #PROMPTS USER TO LOGIN
        nickname = username.nickname()
        self.response.write(FORM_HTML.substitute(action="",
                                                 method="post"))
        self.response.write("Welcome "+ nickname)
        self.response.write("<br>Please enter your 9 digit RIN")                    #PROMPTS USER FOR RIN
        self.response.write(TEXTBOX_HTML.substitute(name="rin",
                                                    row=1,
                                                    col=9,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Sign Up"))
        self.response.write(CLOSE_FORM_HTML)

    def get(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.__write_submission__()
        self.response.write(CLOSE_HTML)
        
    def post(self):
        rin = self.request.get("rin")
        self.response.write(OPEN_HTML.substitute(head=""))                          #VERIFIES RIN FORMAT IS CORRECT
        if len(rin)!=9:
            self.response.write("[ERROR] RIN is 9 digits long")
        elif not(rin.isnumeric()):
            self.response.write("[ERROR] RIN must be all numbers")
        else:
            username = users.get_current_user()
            nickname = username.nickname()
            user = userclass.User(parent=userclass.user_key(nickname))
            user.rin=rin
            user.put()
            self.redirect("/")
        self.__write_submission__()                                                 #SUBMITS
        self.response.write(CLOSE_HTML)
