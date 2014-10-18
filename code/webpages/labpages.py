import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import questions

"""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
"""

QUESTION_HTML = """\
<html>
  <body>
    <form action="" method="post">
      If Albert picks choice 2, Charles picks the choice above Bert, and Debby chooses the choice below Albert, which choice will Eugene select to ensure at least one of them gets the correct answer for every question? <br>
      <input type="radio" name="q1" value="c">Choice 1<br>
      <input type="radio" name="q1" value="w">Choice 2<br>
      <input type="radio" name="q1" value="w">Choice 3<br>
      <input type="radio" name="q1" value="w">Choice 4<br>
      <input type="radio" name="q1" value="w">Choice 5<br>
      The answer to this question is a liar. <br>
      <input type="radio" name="q2" value="w">Choice 2 tells the truth<br>
      <input type="radio" name="q2" value="w">The liar is between 2 truths<br>
      <input type="radio" name="q2" value="c">This choice does not lie<br>
      <input type="radio" name="q2" value="c">Choice 3 is a liar<br>
      <input type="radio" name="q2" value="w">The liar is one of the two choices above.<br>

      <div><input type="submit" value="Submit"></div>
    </form>
  </body>
</html>

"""

class StaticLabPage(webapp2.RequestHandler):
    def getLabID(self):
        my_url = self.request.uri
        lab_id = my_url[len(my_url)-2]
        return int(lab_id)
    def get(self):
        #self.response.write(QUESTION_HTML)
        self.num=0
        self.response.write('<html><body><form action="" method="post">')
        lab_id = self.getLabID()
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(lab_id)).order(questions.Question.number)
        question_list = questions_query.fetch()
        for question in question_list:
            self.num=self.num+1
            self.response.write(question.question)
            for i in range(len(question.choices)):
                ans='w'
                if i+1 in question.answers:
                    ans='c'
                self.response.write('<br><input type="radio" name="q' + str(question.number)+'" value="'+ans+'">'+question.choices[i]+'<br>')
        self.response.write('<br><div><input type="submit" value="Submit"></div>')
        self.response.write('</form></body></html>')
    def post(self):
        questions_query = questions.Question.query(
            ancestor=questions.lab_key(self.getLabID())).order(questions.Question.number)
        question_list = questions_query.fetch()
        for i in range(len(question_list)):
            if self.request.get('q'+str(i+1))=='c':
                self.response.write('correct')
            else:
                self.response.write('wrong')
            self.response.write('<br>')


class DynamicLabPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('dynamic meow<br>')
        self.response.write(self.request.uri)
