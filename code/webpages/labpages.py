import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions
from html import *
#Skeleton of the algorithm for showing a lab
class LabPage(webapp2.RequestHandler):
    #Gets the id of the lab from the url
    def getLabID(self):
        my_url = self.request.uri
        lab_id = my_url[len(my_url)-3:len(my_url)-1]
        return int(lab_id)

    #print all of the information for the lab
    def get(self):
        self.num=0
        #starts off the webpage with a form
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.gatherQuestions()
        
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
                                                          value=ans,
                                                          text=question.choices[i]))
            self.response.write("<br>")

        #submit button
        self.response.write(SUBMIT_HTML.substitute(value="Submit"))

        #end of page
        self.response.write("</form>")
        self.response.write(CLOSE_HTML)
    
    #After submission page
    def post(self):
        #query for the number of questions
        self.gatherQuestions()
        #checks if each answer is correct or wrong
        for i in range(len(self.question_list)):
            if self.request.get("q"+str(i+1))=="correct":
                self.response.write("correct")
            else:
                self.response.write("wrong")
            self.response.write("<br>")


#Implements the gatherQuestions function to select questions based on 
#lab id
class StaticLabPage(LabPage):
    def gatherQuestions(self):
        #gets the questions for the specific lab ID
        lab_id = self.getLabID()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id)).order(questions.Question.number)
        self.question_list = questions_query.fetch()

#Implements the gatherQuestions function to select questions based on 
#poorly completed topics
class DynamicLabPage(LabPage):
    def gatherQuestions(self):
        self.question_list=[]
