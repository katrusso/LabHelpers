import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic

class AdminPage(webapp2.RequestHandler):
    def get(self):
        if not users.is_current_user_admin(): 
            self.abort(404)
        self.__write_html__()

#admin page that leads to either the topic adder or question adder
class Admin(AdminPage):

    def __write_html__(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="/",
                                                 method="link"))
        #sign out button
        self.response.write(SUBMIT_HTML.substitute(value="Return to Main Page"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(FORM_HTML.substitute(action="/admin/questions",
                                                 method="link"))
        #question adding link
        self.response.write(SUBMIT_HTML.substitute(value="Add Question"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(FORM_HTML.substitute(action="/admin/topic",
                                                 method="link"))
        #topic adding link
        self.response.write(SUBMIT_HTML.substitute(value="Add Topic"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)



