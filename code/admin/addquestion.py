import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic
import lab
import admin

#webpage to add a question
class AddQuestion(admin.AdminPage):
    #prints all of the different inputs
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
    def __write_html__(self):
        lab_id = self.request.get("labid")
        if lab_id!="":
            lab_id=int(lab_id)
        topic_name =self.request.get("t1")
        question_number = self.request.get("q1")
        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Choose Lab Number: <br>")
        lab_query = lab.Lab.query(ancestor=lab.lab_key(1)).order(lab.Lab.id)
        lab_list = lab_query.fetch()
        for lab_object in lab_list:
            is_check = ""
            if lab_object.id==lab_id:
                is_check="checked"
            self.response.write(RADIO_HTML.substitute(name="labid",
                checked=is_check,
                value=lab_object.id,
                text=str(lab_object.id)+". "+lab_object.name))
        self.response.write(RADIO_HTML.substitute(name="labid",
                                                  checked="",
                                                  value=4444,
                                                  text="Practice Problems"))

        self.response.write("Choose Topic: <br>")
        topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
        topic_list = topic_query.fetch()
        for topic_object in topic_list:
            is_check = ""
            if topic_name==topic_object.name:
                is_check="checked"
            self.response.write(RADIO_HTML.substitute(name="topic",
                                                      checked=is_check,
                                                      value=topic_object.name,
                                                      text=topic_object.name))
        question_question=""
        question_choices=["","","","",""]
        question_answers=[]
        if lab_id!="" and lab_id!=4444:
            questions_query = questions.Question.query(
                ancestor=questions.lab_key(lab_id))
            questions_query = questions_query.order(questions.Question.number)
            question_list = questions_query.fetch()
            question=question_list[0]
            for i in question_list:
                if i.number==question_number and i.topic==topic_name:
                    question = i
            question_question = question.question
            question_choices=question.choices
            question_answers=question.answers
            
        self.response.write("Question Number: ")
        self.response.write(TEXTBOX_HTML.substitute(name="number",
                                                    row=1,
                                                    col=5,
                                                    text=question_number))
        self.response.write("Enter Question: <br>")
        self.response.write(TEXTBOX_HTML.substitute(name="question",
                                                    row=5,
                                                    col=60,
                                                    text=question_question))
        for i in range(5):
            n=i+1
            self.response.write("Choice "+str(n)+": <br>")
            self.response.write(TEXTBOX_HTML.substitute(name="choice",
                                                        row=3,
                                                        col=60,
                                                        text=question_choices[i]))
            is_check=""
            if n in question_answers:
                is_check="checked"
            self.response.write(CHECKBOX_HTML.substitute(name="correct",
                                                         value=n,
                                                         checked=is_check,
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
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id))
        questions_query = questions_query.order(questions.Question.number)
        question_list = questions_query.fetch()
        is_found=False
        for i in question_list:
            if i.number==number and i.topic==topic_name:
                is_found=True
                i.question=question_str
                i.choices=choice_strs
                i.answers=correct_answers
                i.put()
                break
        if not(is_found):
            question = questions.Question(parent=questions.lab_key(lab_id))
            question.number = number
            question.question = question_str
            question.choices = choice_strs
            question.answers = correct_answers
            question.topic = topic_name
            question.put()
        self.redirect(self.request.uri)
