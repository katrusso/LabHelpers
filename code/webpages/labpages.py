import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions
import userclass

from html_constants import *

#Skeleton of the algorithm for showing a lab
class LabPage(webapp2.RequestHandler):
            
    #print all of the information for the lab
    def get(self):
        self.num=0
        #starts off the webpage with a form
        
        user_object =self.__check_login__()
        lab_responses=self.__get_responses__(user_object)
        self.__gather_questions__()
        if len(lab_responses)!=0 and len(lab_responses[0].responses)==len(self.question_list):
            self.post()
            return
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))

        
        #run through each question creating a multiple choice question for it
        for question in self.question_list:
            self.num=self.num+1
            self.response.write(str(self.num)+". ")
            self.response.write(question.question)
            self.response.write("<br>")
            for i in range(len(question.choices)):
                ans="wrong"
                if i+1 in question.answers:
                    ans="correct"
                self.response.write(RADIO_HTML.substitute(name="q"+str(self.num),
                                                          value=str(i)+ans,
                                                          text=question.choices[i]))
            self.response.write("<br>")

        #submit button
        self.response.write(SUBMIT_HTML.substitute(value="Submit"))

        #end of page
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
    
    #After submission page
    def post(self):
        #query for the number of questions
        lab_id = self.__get_labID__()
        user_object =self.__check_login__()
        self.__gather_questions__()
        topics = []
        totals = []
        select = []
        correct = []
        correct_answers=[]
        is_add=True
        lab_responses = self.__get_responses__(user_object)
        #checks if each answer is correct or wrong
        if len(lab_responses)==0 or len(lab_responses[0].responses)<len(self.question_list):
            for i in range(len(self.question_list)):
                j=0
                for j in range(len(topics)+1):
                    if j==len(topics) or topics[j]==self.question_list[i].topic:
                        break
                        
                if j>=len(topics):
                    topics.append(self.question_list[i].topic)
                    totals.append(1)
                    correct.append(0)
                else:
                    totals[j]=totals[j]+1
                answer = self.request.get("q"+str(i+1))
                if answer!="":
                    select.append(int(answer[0]))
                else:
                    select.append(-1)
                if answer[1:]=="correct":
                    correct[j] = correct[j]+1
                    correct_answers.append(True)
                else:
                    correct_answers.append(False)
        else:
            is_add=False
            for i in range(len(self.question_list)):
                j=0
                for j in range(len(topics)+1):
                    if j==len(topics) or topics[j]==self.question_list[i].topic:
                        break
                if j>=len(topics):
                    topics.append(self.question_list[i].topic)
                    totals.append(1)
                    correct.append(0)
                else:
                    totals[j]=totals[j]+1
                select.append(lab_responses[0].responses[i])
                correct_answers.append(lab_responses[0].correct[i])
                if lab_responses[0].correct[i]:
                    correct[j]=correct[j]+1
                
        #Print the results of the lab
        self.response.write(ALIGN_HTML.substitute(align="center"))
        if lab_id==4444:
            self.response.write("<b><ins> Practice lab results </ins></b><br>")
        else:
            self.response.write("<b><ins>Lab "+str(lab_id)+" results</ins></b><br>")
        self.response.write(OPEN_TABLE_HTML.substitute(percent=50))
        self.response.write("<tr>")
        for i in topics:
            self.response.write(TABLE_COLUMN_HTML.substitute(text=i))
        self.response.write("</tr>")
        self.response.write("<tr>")
        for i in range(len(topics)):
            temp_val = correct[i]*100.0/totals[i]
            self.response.write(TABLE_COLUMN_HTML.substitute(
                text = str(temp_val)+"%"))
        self.response.write("</tr>")
        self.response.write(CLOSE_TABLE_HTML)
        self.response.write("</div>")

        #rewrite each question bolding the correct answer and marking the selected choice
        num=0
        for j in range(len(self.question_list)):
            question = self.question_list[j]
            num=num+1
            self.response.write(str(num)+". ")
            self.response.write(question.question)
            self.response.write("<br>")
            for i in range(len(question.choices)):
                self.response.write(TAB_HTML)
                if i+1 in question.answers:
                    self.response.write('<b>')
                if select[j]==i:
                    self.response.write('<mark>')
                self.response.write(question.choices[i])
                if select[j]==i:
                    self.response.write('</mark>')
                if i+1 in question.answers:
                    self.response.write("</b>")
                self.response.write("<br>")
            self.response.write("<br>")
        if is_add:
            self.__add_responses__(user_object,lab_id,select,correct_answers)
        #if this is a static lab write the topics and practice lab button
        if lab_id!=4444:
            self.response.write(FORM_HTML.substitute(action="/DynamicLab/"
                                                     +str(lab_id)+"/",
                                                     method="link"))
            for i in range(len(topics)):
                isCheck=""
                if correct[i]*100.0/totals[i]<50:
                    isCheck="checked"
                self.response.write(CHECKBOX_HTML.substitute(name="topics",
                                                             checked=isCheck,
                                                             value=topics[i],
                                                             text=topics[i]))
            self.response.write(SUBMIT_HTML.substitute(value="Get Practice Problems"))
            self.response.write(CLOSE_FORM_HTML)
        #otherwise write button to the main page
        else:
            self.response.write(FORM_HTML.substitute(action="/",method="link"))
            self.response.write(SUBMIT_HTML.substitute(value="Return to main page"))
            self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)

    def __check_login__(self):
        username = users.get_current_user()
        return userclass.__sign_in__(self,username.nickname())
        
#Implements the gatherQuestions function to select questions based on 
#lab id
class StaticLabPage(LabPage):
    #Gets the id of the lab from the url
    def __get_labID__(self):
        my_url = self.request.uri
        lab_id = my_url[len(my_url)-3:len(my_url)-1]
        return int(lab_id)

    def __get_responses__(self,user_object):
        username = users.get_current_user()
        return user_object[0].query_responses(self.__get_labID__(),username.nickname())
    def __add_responses__(self,user_object,lab_id,responses,correct):
        username = users.get_current_user()
        user_object[0].__add_responses__(lab_id,username.nickname(),responses,correct)
    def __gather_questions__(self):
        #gets the questions for the specific lab ID
        lab_id = self.__get_labID__()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id)).order(questions.Question.number)
        self.question_list = questions_query.fetch()

#Implements the gatherQuestions function to select questions based on 
#poorly completed topics
class DynamicLabPage(LabPage):
    #Gets the id of the lab from the url
    def __get_labID__(self):
        return 4444
    def __get_responses__(self,user_object):
        return []
    def __add_responses__(self,user_object,lab_id,responses,correct):
        return;
    def __gather_questions__(self):
        self.question_list=[]
        lab_id=4444
        topics = self.request.get_all("topics")
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(4444)).order(questions.Question.topic)
        temp_list = questions_query.fetch()
        for i in temp_list:
            if i.topic in topics:
                self.question_list.append(i)
