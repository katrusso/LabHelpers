
from google.appengine.ext import ndb

def topic_key(topic_id=0):
    return ndb.Key('Topic',topic_id)

class Topic(ndb.Model):
    name = ndb.StringProperty()
    
