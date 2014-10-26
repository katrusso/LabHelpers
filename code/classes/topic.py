
from google.appengine.ext import ndb

import topic

def topic_key():
    return ndb.Key('Topic')

class Topic(ndb.Model):
    number = ndb.IntegerProperty()
    question = ndb.StringProperty()
    choices = ndb.StringProperty(repeated=True)
    answers = ndb.IntegerProperty(repeated=True)
    
