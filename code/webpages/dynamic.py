import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2                                                                  #FRAMEWORK

import labpages                                                                 #RELEVANT CLASSES
import questions
import userclass
from html_constants import *                                                    #REDUCES CODE REDUNDANCIES


class DynamicLabPage(labpages.LabPage):
    '''
    THIS CLASS IMPLEMENTS THE GATHER-QUESTIONS FUNCTION TO SELECT CUSTOM PRACTICE 
    QUESTIONS FROM THE DATASTORE BASED ON THE USER'S POOR PERFORMANCE IN SPECIFIC TOPICS.  
    THIS ASSESSMENT IS BASED ON THE GRADING (BY TOPIC) OF THE STUDENT'S PRECURSORY 
    STATIC LAB.
    '''
    
    def __get_labID__(self):                                                        
        return 4444
    def __get_lab_name__(self):
        return "Practice Problems"
    def __write_header__(self):
        write_css_html(self,"Practice Problems")
    def __get_responses__(self,user_object):
        return []
    def __add_responses__(self,user_object,lab_id,responses,correct):
        return;
    def __gather_questions__(self,sort_by_topic):
        self.question_list=[]
        lab_id=4444
        topics = self.request.get_all("topics")
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(4444)).order(questions.Question.topic)
        temp_list = questions_query.fetch()
        for i in temp_list:
            if i.topic in topics:
                self.question_list.append(i)
