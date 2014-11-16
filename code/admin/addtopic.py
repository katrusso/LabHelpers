import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *
import questions
import topic
import coach
import admin

#interface for the topic adding (works the same way as the question one
class AddTopic(admin.AdminPage):
    def __write_link_to_admin__(self):
        self.response.write(LINK_HTML.substitute(link="/admin",
                                                 text="Return to Admin Page"))
        self.response.write("<br>")
    def __write_html__(self):

        self.response.write(OPEN_HTML.substitute(head=""))
        self.response.write(FORM_HTML.substitute(action="",method="post"))
        self.response.write("Enter topic name:")
        topic_name = self.request.get("t1")
        equations =["","","","",""]
        summary=""
        example=""
        if topic_name!="":
            coach_query = coach.Coach.query(
                ancestor=coach.topic_key(topic_name))
            coach_list = coach_query.fetch()
            if len(coach_list)!=0:
                equations = coach_list[0].equations
                summary =coach_list[0].summary
                example =coach_list[0].example
        
        self.response.write(TEXTBOX_HTML.substitute(name="topic",
                                                    row=1,
                                                    col=30,
                                                    text=topic_name))
        self.response.write("Enter in related equations:<br>")
        for i in range(5):
            self.response.write(TEXTBOX_HTML.substitute(name="equation",
                                                        row=1,
                                                        col=50,
                                                        text=equations[i]))
        self.response.write("Summary of Topic:<br>")
        self.response.write(TEXTBOX_HTML.substitute(name="summary",
                                                    row=5,
                                                    col=100,
                                                    text=summary))
        self.response.write("Example for topic:<br>")
        self.response.write(TEXTBOX_HTML.substitute(name="example",
                                                    row=10,
                                                    col=100,
                                                    text=example))
        self.response.write(SUBMIT_HTML.substitute(value="Add topic"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)
    def post(self):
        topic_name=self.request.get('topic')
        topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
        topic_list = topic_query.fetch()
        isFound=False
        for topic_object in topic_list:
            if topic_object.name==topic_name:
                isFound=True
        if isFound==False:
            topic_object = topic.Topic(parent=topic.topic_key(1))
            topic_object.name = topic_name
            topic_object.put()
        equations=self.request.get_all("equation")
        summary=self.request.get("summary")
        example=self.request.get("example")
        coach_object = coach.Coach(parent=coach.topic_key(topic_name))
        if isFound==True:
            coach_query = coach.Coach.query(
                ancestor=coach.topic_key(topic_name))
            coach_object = coach_query.fetch()[0]
        
        coach_object.equations=equations
        self.response.write(coach_object.equations)
        coach_object.summary=summary
        coach_object.example=example
        coach_object.put()
        my_url = self.request.uri
        if my_url.rfind('?')!=-1:
            self.redirect(my_url[0:my_url.rfind('?')])
        else:
            self.redirect(my_url)
