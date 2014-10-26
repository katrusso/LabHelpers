import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions
from html import *

class StaticLabPage(webapp2.RequestHandler):
    #Gets the id of the static lab from the url
    def getLabID(self):
        my_url = self.request.uri
        lab_id = my_url[len(my_url)-3:len(my_url)-1]
        return int(lab_id)

    #function that is run at beginning of webpage
    def get(self):
        self.num=0
        #starts off the webpage with a form
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))

        #gets the questions for the specific lab ID
        lab_id = self.getLabID()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id)).order(questions.Question.number)
        question_list = questions_query.fetch()
        #run through each question creating a multiple choice question for it
        for question in question_list:
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
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(self.getLabID())).order(questions.Question.number)
        question_list = questions_query.fetch()

        #checks if each answer is correct or wrong
        for i in range(len(question_list)):
            if self.request.get("q"+str(i+1))=="correct":
                self.response.write("correct")
            else:
                self.response.write("wrong")
            self.response.write("<br>")


class DynamicLabPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('dynamic meow<br>')
        self.response.write(self.request.uri)
