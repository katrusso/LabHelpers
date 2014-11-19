import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2                                                                      #FRAMEWORK
import coach                                                                        #RELEVANT CLASS
from html_constants import *                                                        #REDUCES CODE REDUNDANCY ACROSS FILES

MAX_CHARACTERS = 80

class LabTopic(webapp2.RequestHandler):
    '''
    AS SEEN IN LABPAGES.PY, AFTER THE USER SUBMITS THEIR COMPLETED LAB A SMALL DASHBOARD
    OF THEIR GRADES PER SECTION APPEARS AT THE TOP OF THE CORRECTED LAB. 
    
    WITHIN THE DASHBOARD IS A TABULAR LIST OF TOPICS; THEY ARE CLICKABLE LINKS.
    BELOW THEM THE USER'S GRADE FOR QUESTIONS ASSOCIATED WITH THAT TOPIC.
    
    THE PURPOSE OF THIS CLASS IS TO OPEN THE "COACH DATA" WEBPAGE IN THE SAME TAB WHEN A 
    USER CLICKS ON A TOPIC-LINK IN THE GRADE-DASHBOARD OF THEIR CORRECTED LAB. 
    
    THE COACH DATA CONTAINS THE TOPIC NAME, RELEVANT FORMULAS, AN EXPLANATION OF THE 
    TOPIC'S FUNDAMENTAL CONCEPTS, AND AN EXAMPLE. 
    
    THE INTENTION HERE BEING TO HELP THE STUDENT RECOGNIZE THE SOURCE OF THEIR ERRORS 
    WITHOUT REQUIRING ADDITIONAL RESOURCES. 
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
