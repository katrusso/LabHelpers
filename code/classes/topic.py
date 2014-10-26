
from google.appengine.ext import ndb

import topic

def topic_key():
    return ndb.Key('Topic')

class Topic(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    
