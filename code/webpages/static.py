import os
import urllib
import cgi
from google.appengine.api import users                          
from google.appengine.ext import ndb                                                #ENABLES INTERACTION WITH DATASTORE

import webapp2                                                                      #FRAMEWORK

import lab                                                                          #RELEVANT CLASSES
import questions
import userclass
import labpages
from html_constants import *                                                        #REDUCES CODE REDUNDANCIES


class StaticLabPage(labpages.LabPage):
    '''
    THIS CLASS IMPLEMENTS THE GATHER-QUESTIONS FUNCTION TO SELECT LAB QUESTIONS FROM THE 
    DATASTORE BASED ON THE LAB ID (RETRIEVED FROM THE LAB URL USER CLICKS THROUGH ON 
    MAINPAGE)
    '''
    def __get_labID__(self):                                                        #GETS THE ID OF THE LAB FROM THE URL
        my_url = self.request.uri
        ind = my_url[0:len(my_url)-1].rfind('/')
        lab_id = my_url[ind+1:(len(my_url)-1)]
        return int(lab_id)
        
    def __get_lab_name__(self):                                                     #GETS LAB NAME
        lab_query = lab.Lab.query(ancestor=lab.lab_key(1)).order(lab.Lab.id)
        lab_list = lab_query.fetch()
        for i in lab_list:
            if i.id==self.__get_labID__():
                lab_object=i
        return lab_object.name
        
    def __write_header__(self):                                                     #POPULATES PAGE HEADER
        lab_name = self.__get_lab_name__()
        write_css_html(self,"Lab "+str(self.__get_labID__())+
            ": "+lab_name) 
            
    def __get_responses__(self,user_object):                                        #GETS USER RESPONSES
        username = users.get_current_user()
        return user_object[0].__query_responses__(self.__get_labID__(),username.nickname())
        
    def __add_responses__(self,user_object,lab_id,responses,correct):               #SAVES USER RESPONSES
        username = users.get_current_user()
        user_object[0].__add_responses__(lab_id,username.nickname(),responses,correct)
        
    def __gather_questions__(self,sort_by_topic):                                   #GETS THE QUESTIONS ASSOCIATED WITH THE SPECIFIC LAB ID
        lab_id = self.__get_labID__()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id))
        questions_query = questions_query.order(questions.Question.number)
        self.question_list = questions_query.fetch()
