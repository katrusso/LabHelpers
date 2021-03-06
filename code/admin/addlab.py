import os
import urllib
import cgi
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import lab
import admin


class AddLab(admin.AdminPage):
    '''
    THIS CLASS PROVIDES AN INTERFACE FOR ALLOWING AN ADMIN USER TO ADD A LAB AND ITS 
    RESPECTIVE ATTRIBUTES (ID, NAME) TO THE DATASTORE (AND BY EXTENSION, THE WEBSITE)
    '''
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
    
    def __write_html__(self):

        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Enter lab number:")
        self.response.write(TEXTBOX_HTML.substitute(name="lab_id",
                                                    row=1,
                                                    col=4,
                                                    text=""))
        self.response.write("Enter the lab name:")
        self.response.write(TEXTBOX_HTML.substitute(name="lab_name",
                                                    row=1,
                                                    col=30,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Add Lab"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
    
    def post(self):
        lab_id=int(self.request.get("lab_id"))
        lab_name=self.request.get("lab_name")
        lab_object = lab.Lab(parent=lab.lab_key(1))
        lab_object.id=lab_id
        lab_object.name = lab_name
        lab_object.put()
        self.redirect(self.request.uri)
