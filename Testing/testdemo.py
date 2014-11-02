######################################################
###  ALL TEST NAMES MUST START WITH THE WORD TEST  ###
######################################################
############  AND NO SPECIAL CHARACTERS  #############
######################################################
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class DemoTestCase(unittest.TestCase):

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

  def test1Example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

  def test2Example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

  def test3Example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
