import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html import *
import questions

class Admin(webapp2.RequestHandler):
    def get(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="/",
                                                 method="post"))
        self.response.write(SUBMIT_BUTTON_HTML.substitute(value="Sign Out"))
        self.response.write('</form>')
        self.response.write(FORM_HTML.substitute(action="/admin/questions",
                                                 method="link"))
        self.response.write(SUBMIT_BUTTON_HTML.substitute(value="Add Question"))
        self.response.write("</form>")
        self.response.write(FORM_HTML.substitute(action="/admin/topic",
                                                 method="link"))
        self.response.write(SUBMIT_BUTTON_HTML.substitute(value="Add Topic"))
        self.response.write("</form>")
        self.response.write(CLOSE_HTML)

class AddQuestion(webapp2.RequestHandler):
    def get(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Choose Lab Number: <br>")
        self.response.write(RADIO_BUTTON_HTML.substitute(name="labid",
                                                         value=1,
                                                         text="Test Lab"))
        self.response.write(RADIO_BUTTON_HTML.substitute(name="labid",
                                                         value=17,
                                                         text="Lab 17"))
        self.response.write(RADIO_BUTTON_HTML.substitute(name="labid",
                                                         value=4444,
                                                         text="Practice Problems"))
        self.response.write("Question Number: ")
        self.response.write(TEXTBOX_HTML.substitute(name="number",
                                                    row=1,
                                                    col=5,
                                                    text=""))
        self.response.write("Enter Question: <br>")
        self.response.write(TEXTBOX_HTML.substitute(name="question",
                                                    row=5,
                                                    col=60,
                                                    text=""))
        for i in range(5):
            n=i+1
            self.response.write("Choice "+str(n)+": <br>")
            self.response.write(TEXTBOX_HTML.substitute(name="choice",
                                                        row=3,
                                                        col=60,
                                                        text=""))
            self.response.write(CHECKBOX_HTML.substitute(name="correct",
                                                         value=n,
                                                         text="Choice is correct"))
        self.response.write(SUBMIT_BUTTON_HTML.substitute(value="Add question"))
        self.response.write("</form>")
        self.response.write(CLOSE_HTML)

    def post(self):
        lab_id = int(self.request.get('labid'))
        number = int(self.request.get('number'))
        question_str = self.request.get('question')
        choice_strs = self.request.get('choice', allow_multiple=True)
        correct_answer_strs = self.request.get('correct', allow_multiple=True)
        correct_answers = [];
        for i in range(len(correct_answer_strs)):
            correct_answers.append(int(correct_answer_strs[i]))
        question = questions.Question(parent=questions.lab_key(lab_id))
        question.number = number
        question.question = question_str
        question.choices = choice_strs
        question.answers = correct_answers
        question.put()
        self.redirect(self.request.uri)

class AddTopic(webapp2.RequestHandler):
    def get(self):
        self.response.write('bleh')
