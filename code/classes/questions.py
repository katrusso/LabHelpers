
from google.appengine.ext import ndb

import topic

def lab_key(labid=0):
    return ndb.Key('Labs', labid)

class Question(ndb.Model):
    number = ndb.IntegerProperty()
    question = ndb.StringProperty()
    choices = ndb.StringProperty(repeated=True)
    answers = ndb.IntegerProperty(repeated=True)
#    topic = ndb.StructuredProperty(topic.Topic)
