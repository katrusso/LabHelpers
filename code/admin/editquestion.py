import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
from string import Template

from html_constants import *

import topic
import admin
import lab
import questions

class EditQuestion(admin.AdminPage):
    '''
    THIS CLASS PROVIDES AN INTERFACE FOR ALLOWING AN ADMIN USER TO EDIT THE 
    DATASTORE CONTENT: QUESTIONS AND QUESTION ATTRIBUTES.
    '''
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
        
    def __write_html__(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.__write_select__(-1,"")
        self.response.write(SUBMIT_HTML.substitute(value="List Questions"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
    
    def post(self):                                                                 #RETRIEVES QUESTIONS FOR THE SPECIFIC LAB ID
        lab_id = int(self.request.get("labid"))
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id))
        questions_query = questions_query.order(questions.Question.number)
        question_list = questions_query.fetch()
        topic_name = self.request.get("t1")
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="/admin/questions",
                                                 method="get"))
        self.__write_link_to_admin__()
        self.__write_select__(lab_id,topic_name)
        self.response.write("<br>Choose question:<br>")
        for question in question_list:
            if topic_name==question.topic:
                self.response.write(RADIO_HTML.substitute(
                    name="q1",
                    checked="",
                    value=question.number,
                    text=str(question.number) + ". " + question.question[0:20]))
        self.response.write(SUBMIT_HTML.substitute(value="Edit Question"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)    

    def __write_select__(self,lab_id,topic_name):
        self.response.write("<br>Choose lab number:<br>")
        lab_query = lab.Lab.query(ancestor=lab.lab_key(1)).order(lab.Lab.id)
        lab_list = lab_query.fetch()
        for lab_object in lab_list:
            is_check=""
            if lab_id==lab_object.id:
                is_check="checked"
            self.response.write(RADIO_HTML.substitute(
                name="labid",
                checked=is_check,
                value=lab_object.id,
                text=str(lab_object.id)+". "+lab_object.name))
        is_check=""
        if lab_id==4444:
            is_check="checked"
        self.response.write(RADIO_HTML.substitute(name="labid",checked=is_check,
                                                  value=4444,
                                                  text="Practice Problems"))
        self.response.write("<br>Choose topic name:<br>")
        topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
        topic_list = topic_query.fetch()
        for topic_object in topic_list:
            is_check=""
            if topic_name==topic_object.name:
                is_check="checked"
            self.response.write(RADIO_HTML.substitute(name="t1",
                                                      checked=is_check,
                                                      value=topic_object.name,
                                                      text=topic_object.name))
        
