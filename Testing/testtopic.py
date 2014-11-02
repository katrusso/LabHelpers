import unittest
import topic
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.datastore import datastore_stub_util


class TopicClassTest(unittest.TestCase):

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
    topic_object = topic.Topic(parent=topic.topic_key(1))
    topic_object.name = "First"
    topic_object.put()
    topic_object2 = topic.Topic(parent=topic.topic_key(2))
    topic_object2.name = "Second"
    topic_object2.put()
    topic_object3 = topic.Topic(parent=topic.topic_key(2))
    topic_object3.name = "SecondSecond"
    topic_object3.put()
    topic_object4 = topic.Topic(parent=topic.topic_key(3))
    topic_object4.name = "Third"
    topic_object4.put()

    ###TEST VALUES###
    topic_query = topic.Topic.query(ancestor=topic.topic_key(1))
    topic_list = topic_query.fetch()
    self.assertEqual(len(topic_list),1)
    self.assertEqual(topic_list[0].name,"First")
    ################################################3
    topic_query = topic.Topic.query(ancestor=topic.topic_key(2))
    topic_list = topic_query.fetch()
    self.assertEqual(len(topic_list),2)
    self.assertEqual(topic_list[0].name,"Second")
    self.assertEqual(topic_list[1].name,"SecondSecond")
    ################################################3
    topic_query = topic.Topic.query(ancestor=topic.topic_key(3))
    topic_list = topic_query.fetch()
    self.assertEqual(len(topic_list),1)
    self.assertEqual(topic_list[0].name,"Third")
    
if __name__ == '__main__':
    unittest.main()
