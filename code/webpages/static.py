import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions
import userclass
import labpages
from html_constants import *

#Implements the gatherQuestions function to select questions based on 
#lab id
class StaticLabPage(labpages.LabPage):
    #Gets the id of the lab from the url
    def __get_labID__(self):
        my_url = self.request.uri
        ind = my_url[0:len(my_url)-1].rfind('/')
        lab_id = my_url[ind+1:(len(my_url)-1)]
        return int(lab_id)

    def __get_responses__(self,user_object):
        username = users.get_current_user()
        return user_object[0].__query_responses__(self.__get_labID__(),username.nickname())
    def __add_responses__(self,user_object,lab_id,responses,correct):
        username = users.get_current_user()
        user_object[0].__add_responses__(lab_id,username.nickname(),responses,correct)
    def __gather_questions__(self,sort_by_topic):
        #gets the questions for the specific lab ID
        lab_id = self.__get_labID__()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id))
        questions_query = questions_query.order(questions.Question.number)
        self.question_list = questions_query.fetch()
