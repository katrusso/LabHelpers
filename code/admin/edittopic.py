import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *

import topic
import coach
import admin


class EditTopic(admin.AdminPage):
    '''
    THIS CLASS PROVIDES AN INTERFACE FOR ALLOWING AN ADMIN USER TO EDIT THE 
    DATASTORE CONTENT: TOPICS AND TOPIC ATTRIBUTES.
    '''
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
    def __write_html__(self):

        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="/admin/topic",method="get"))
        self.response.write("Choose topic name:<br>")
        topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
        topic_list = topic_query.fetch()
        for topic_object in topic_list:
            self.response.write(RADIO_HTML.substitute(name="t1",
                                                      checked="",
                                                      value=topic_object.name,
                                                      text=topic_object.name))
        self.response.write(SUBMIT_HTML.substitute(value="Search for topic"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
