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

        self.response.write(LINK_HTML.substitute(link="/",
                                                 text="Return to Main Page<br>"))
        self.response.write(LINK_HTML.substitute(link="/admin/lab",
                                                 text="Add Lab<br>"))
        self.response.write(LINK_HTML.substitute(link="/admin/topic",
                                                 text="Add Topic<br>"))        
        self.response.write(LINK_HTML.substitute(link="/admin/questions",
                                                 text="Add Question<br>"))
        self.response.write(CLOSE_HTML)



