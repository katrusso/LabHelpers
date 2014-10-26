import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions
from html_constants import *
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
        lab_id = self.getLabID()
        self.gatherQuestions()
        self.topics = []
        self.totals = []
        self.correct = []
        #checks if each answer is correct or wrong
        for i in range(len(self.question_list)):
            j=0
            for j in range(len(self.topics)+1):
                if j==len(self.topics) or self.topics[j]==self.question_list[i].topic:
                    break
            
            if j>=len(self.topics):
                self.topics.append(self.question_list[i].topic)
                self.totals.append(1)
                self.correct.append(0)
            else:
                self.totals[j]=self.totals[j]+1
            if self.request.get("q"+str(i+1))=="correct":
                self.response.write("correct")
                self.correct[j] = self.correct[j]+1
            else:
                self.response.write("wrong")
            self.response.write("<br>")
        self.response.write(ALIGN_HTML.substitute(align="center"))
        self.response.write(TABLE_COLUMN_HTML.substitute(
            text="<b><ins>Lab "+str(lab_id)+" results</ins></b>"))
        self.response.write(OPEN_TABLE_HTML.substitute(percent=50))
        self.response.write("<tr>")
        self.response.write(TABLE_COLUMN_HTML.substitute(
            text=""))
        
        self.response.write(TABLE_COLUMN_HTML.substitute(
            text=""))
        self.response.write("</tr>")
        self.response.write("<tr>")
        for i in self.topics:
            self.response.write(TABLE_COLUMN_HTML.substitute(text=i))
        self.response.write("</tr>")
        self.response.write("<tr>")
        for i in range(len(self.topics)):
            self.response.write(TABLE_COLUMN_HTML.substitute(
                text = str(self.correct[i]*100.0/self.totals[i])+"%"))
        self.response.write("</tr>")
        self.response.write(CLOSE_TABLE_HTML)
        self.response.write("</div>")
        self.response.write(CLOSE_HTML)
        

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
