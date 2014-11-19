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
    '''
    As seen in labpages.py, after the user submits their completed lab a small dashboard
    of their grades per section appears at the top of the corrected lab. 
    
    Within the dashboard is a tabular list of topics; they are clickable links.
    Below them the user's grade for questions associated with that topic.
    
    The purpose of this class is to open the "coach data" webpage in the same tab when a 
    user clicks on a topic-link in the grade-dashboard of their corrected lab. 
    
    The coach data contains the topic name, relevant formulas, an explanation of the 
    topic's fundamental concepts, and an example. 
    
    The intention here being to help the student recognize the source of their errors 
    without requiring additional resources. 
    '''
    
    def get(self):                                                                  #FETCH COACH DATA ASSOCIATED WITH TOPIC LINK
        my_url = self.request.uri
        ind = my_url.rfind('/')
        topic_name = my_url[ind+1:len(my_url)]
        coach_query = coach.Coach.query(
            ancestor=coach.topic_key(topic_name))
        coach_list = coach_query.fetch()
        if len(coach_list)==0:
            return;
        coach_object = coach_query.fetch()[0]
        
        self.response.write(OPEN_HTML.substitute(head='''<link 
        rel="stylesheet" href="/stylesheets/labtopic.css"/>'''))                    #STYLESHEET - MAIN
        
        write_css_html(self,"<b>"+topic_name+"</b>")                                #INSERTS PAGE HEADING FROM HTML CONSTANTS FILE (ICON + "LAB HELPERS")
        
        
        self.response.write(CSS_CLASS_HTML.substitute(id="coach-body"))             #STYLESHEET - OPEN TAG :: COACH-BODY
        self.response.write(CSS_CLASS_HTML.substitute(id="coach-section"))          #STYLESHEET - OPEN TAG :: COACH-SECTION

        self.response.write("<br><br>Relevant Equations:<br>")
        for i in coach_object.equations:
            self.response.write(i)
            self.response.write("<br>")
        self.__print__(coach_object.summary)
        self.__print__(coach_object.example)
        self.response.write(LINK_HTML.substitute(link=my_url[0:ind+1],
                                                     text="Return to Lab"))
        self.response.write(CLOSE_HTML)
        
        self.response.write(CLOSE_CSS_HTML)                                         #STYLESHEET - CLOSING TAG :: COACH-SECTION
        self.response.write(CLOSE_CSS_HTML)                                         #STYLESHEET - CLOSING TAG :: COACH-BODY

        
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
