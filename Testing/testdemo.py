######################################################
###  ALL TEST NAMES MUST START WITH THE WORD TEST  ###
######################################################
############  AND NO SPECIAL CHARACTERS  #############
######################################################
import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class DemoTestCase(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Initialize the datastore stub with this policy.
    self.testbed.init_all_stubs

  def tearDown(self):
    self.testbed.deactivate()

  def test1example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

  def test2example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

  def test3example(self):
    ###INPUT OF SOMESORT###



    ###TEST VALUES###
    self.assertEqual(1, 1)
    self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
