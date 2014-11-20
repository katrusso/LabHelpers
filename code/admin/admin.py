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
    '''
    THIS CLASS PROVIDES AN INTERFACE FOR ALLOWING AN ADMIN USER TO ADD-TO OR EDIT THE 
    DATASTORE / WEBSITE CONTENT.
    '''
    def get(self):                                                                  #ADMIN USER VERIFICATION
        if not users.is_current_user_admin(): 
            self.abort(403)
        self.__write_link_to_admin__()
        self.response.write("<br>")
        self.__write_html__()


class Admin(AdminPage):                                                             #ADMIN INTERFACE
    def __write_link_to_admin__(self):
        return
    def __write_html__(self):
        self.response.write(OPEN_HTML.substitute(head=""))

        self.response.write(LINK_HTML.substitute(link="/",
                                                 text="Return to Main Page<br>"))
        self.response.write(LINK_HTML.substitute(link="/admin/lab",
                                                 text="Add Lab<br>"))
        self.response.write(LINK_HTML.substitute(link="/admin/topic",
                                                 text="Add Topic"))
        self.response.write(TAB_HTML*2)
        self.response.write(LINK_HTML.substitute(link="/admin/etopic",
                                                 text="Edit Topic<br>"))        
        self.response.write(LINK_HTML.substitute(link="/admin/questions",
                                                 text="Add Question"))
        self.response.write(TAB_HTML)
        self.response.write(LINK_HTML.substitute(link="/admin/equestions",
                                                 text="Edit Question<br>"))
        self.response.write(CLOSE_HTML)



