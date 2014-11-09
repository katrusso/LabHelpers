import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic
import admin

#interface for the topic adding (works the same way as the question one
class AddTopic(admin.AdminPage):
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
    def __write_html__(self):

        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Enter topic name:")
        self.response.write(TEXTBOX_HTML.substitute(name="topic",
                                                    row=1,
                                                    col=30,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Add topic"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
    def post(self):
        topic_name=self.request.get('topic')
        topic_object = topic.Topic(parent=topic.topic_key(1))
        topic_object.name = topic_name
        topic_object.put()
        self.redirect(self.request.uri)
