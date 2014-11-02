import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic
import admin

#webpage to add a question
class AddQuestion(admin.AdminPage):
    #prints all of the different inputs
    def __write_html__(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Choose Lab Number: <br>")
        self.response.write(RADIO_HTML.substitute(name="labid",
                                                  value=1,
                                                  text="Test Lab"))
        self.response.write(RADIO_HTML.substitute(name="labid",
                                                  value=17,
                                                  text="Lab 17"))
        self.response.write(RADIO_HTML.substitute(name="labid",
                                                  value=4444,
                                                  text="Practice Problems"))

        self.response.write("Choose Topic: <br>")
        topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
        topic_list = topic_query.fetch()
        for topic_object in topic_list:
            self.response.write(RADIO_HTML.substitute(name="topic",
                                                      value=topic_object.name,
                                                      text=topic_object.name))

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
                                                         checked="",
                                                         text="Choice is correct"))
        self.response.write(SUBMIT_HTML.substitute(value="Add question"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)

    #pushes question into the datastore and reload the web page
    def post(self):
        lab_id = int(self.request.get('labid'))
        number = int(self.request.get('number'))
        topic_name = self.request.get('topic')
        question_str = self.request.get('question')
        choice_strs = self.request.get_all('choice')
        correct_answer_strs = self.request.get_all('correct')
        correct_answers = [];
        for i in range(len(correct_answer_strs)):
            correct_answers.append(int(correct_answer_strs[i]))
        question = questions.Question(parent=questions.lab_key(lab_id))
        question.number = number
        question.question = question_str
        question.choices = choice_strs
        question.answers = correct_answers
        question.topic = topic_name
        question.put()
        self.redirect(self.request.uri)
