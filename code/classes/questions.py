from google.appengine.ext import ndb

import topic

def lab_key(labid=0):
    return ndb.Key('Labs', labid)

def lab_key_topic(topic):
    return ndb.Key('Labs',4444)

class Question(ndb.Model):
    number = ndb.IntegerProperty()
    topic = ndb.StringProperty()
    question = ndb.StringProperty()
    choices = ndb.StringProperty(repeated=True)
    answers = ndb.IntegerProperty(repeated=True)
