import unittest
import questions
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.datastore import datastore_stub_util


class QuestionClassTest(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Create a consistency policy that will simulate the High Replication consistency model.
    self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
    # Initialize the datastore stub with this policy.
    self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testCreationAndRetrieval(self):
    ###INPUT OF SOMESORT###
    question = questions.Question(parent=questions.lab_key(1))
    question.number = 1
    question.question = "NO"
    question.choices = ["1","2","3","4"]
    question.answers = [0]
    question.topic = "MEOW"
    question.put()
    ###TEST VALUES###
    questions_query = questions.Question.query(
        ancestor=questions.lab_key(1)).order(questions.Question.number)
    question_list = questions_query.fetch()
    ################################################3
    q = question_list[0]
    self.assertEqual(question.number , 1)
    self.assertEqual(question.question , "NO")
    self.assertEqual(question.choices , ["1","2","3","4"])
    self.assertEqual(question.answers , [0])
    self.assertEqual(question.topic , "MEOW")

 
    
if __name__ == '__main__':
    unittest.main()

