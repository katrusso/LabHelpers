import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic

#admin page that leads to either the topic adder or question adder
class Admin(webapp2.RequestHandler):
    def get(self):
        if not users.is_current_user_admin(): 
                self.redirect('/')
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="/",
                                                 method="link"))
        #sign out button
        self.response.write(SUBMIT_HTML.substitute(value="Return to Main Page"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(FORM_HTML.substitute(action="/admin/questions",
                                                 method="link"))
        #question adding link
        self.response.write(SUBMIT_HTML.substitute(value="Add Question"))
        self.response.write("</form>")
        self.response.write(FORM_HTML.substitute(action="/admin/topic",
                                                 method="link"))
        #topic adding link
        self.response.write(SUBMIT_HTML.substitute(value="Add Topic"))
        self.response.write("</form>")
        self.response.write(CLOSE_HTML)

#webpage to add a question
class AddQuestion(webapp2.RequestHandler):
    #prints all of the different inputs
    def get(self):
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
        self.response.write("</form>")
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

#interface for the topic adding (works the same way as the question one
class AddTopic(webapp2.RequestHandler):
    def get(self):
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Enter topic name:")
        self.response.write(TEXTBOX_HTML.substitute(name="topic",
                                                    row=1,
                                                    col=30,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Add topic"))
        self.response.write("</form>")
        self.response.write(CLOSE_HTML)
    def post(self):
        topic_name=self.request.get('topic')
        topic_object = topic.Topic(parent=topic.topic_key(1))
        topic_object.name = topic_name
        topic_object.put()
        self.redirect(self.request.uri)
