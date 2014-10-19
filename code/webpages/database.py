import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

import questions

QUESTION_HTML_INPUT="""\
<html>
  <body>
    <form action="" method="post">
      Choose Lab Number: <br>
      <input type="radio" name="labid" value="1">Lab 1<br>
      <input type="radio" name="labid" value="2">Lab 2<br>
      <input type="radio" name="labid" value="3">Lab 3<br>
      <input type="radio" name="labid" value="4">Lab 4<br>
      <input type="radio" name="labid" value="4444">Practice Problem<br>
      Question Number: <div><textarea name="number" rows="1" cols="5"></textarea></div>
      Enter Question: <br>
      <div><textarea name="question" rows="5" cols="60"></textarea></div>
      Choice 1: <br>
      <div><textarea name="choice" rows="3" cols="60"></textarea></div>
      <input type="checkbox" name="correct" value="1">Choice 1 is correct<br>
      Choice 2: <br>
      <div><textarea name="choice" rows="3" cols="60"></textarea></div>
      <input type="checkbox" name="correct" value="2">Choice 2 is correct<br>
      Choice 3: <br>
      <div><textarea name="choice" rows="3" cols="60"></textarea></div>
      <input type="checkbox" name="correct" value="3">Choice 3 is correct<br>
      Choice 4: <br>
      <div><textarea name="choice" rows="3" cols="60"></textarea></div>
      <input type="checkbox" name="correct" value="4">Choice 4 is correct<br>
      Choice 5: <br>
      <div><textarea name="choice" rows="3" cols="60"></textarea></div>
      <input type="checkbox" name="correct" value="5">Choice 5 is correct<br>
      <div><input type="submit" value="Add question"></div>
    </form>
  </body>
</html>
"""
class AddQuestion(webapp2.RequestHandler):
    def get(self):
        self.response.write(QUESTION_HTML_INPUT)

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
        self.response.write(QUESTION_HTML_INPUT)

