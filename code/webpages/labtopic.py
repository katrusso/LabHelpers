import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import coach
from html_constants import *

MAX_CHARACTERS = 80

class LabTopic(webapp2.RequestHandler):
    def get(self):
        my_url = self.request.uri
        ind = my_url.rfind('/')
        topic_name = my_url[ind+1:len(my_url)]
        coach_query = coach.Coach.query(
            ancestor=coach.topic_key(topic_name))
        coach_list = coach_query.fetch()
        if len(coach_list)==0:
            return;
        coach_object = coach_query.fetch()[0]
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(topic_name)
        self.response.write("<br><br>Relavent Equations:<br>")
        for i in coach_object.equations:
            self.response.write(i)
            self.response.write("<br>")
        self.__print__(coach_object.summary)
        self.__print__(coach_object.example)
        self.response.write(LINK_HTML.substitute(link=my_url[0:ind+1],
                                                 text="Return to Lab"))
        self.response.write(CLOSE_HTML)
        
    def __print__(self,string):
        count=0
        for i in string:
            count=count+1
            if i=='\n':
                self.response.write("<br>")
                count=0
            else:
                self.response.write(i)
            if (count>MAX_CHARACTERS and i==' ') or count>MAX_CHARACTERS*1.05:
                count=0
                self.response.write("<br>")
        self.response.write("<br>")
        self.response.write("<br>")
        self.response.write("<br>")
        self.response.write("<br>")
