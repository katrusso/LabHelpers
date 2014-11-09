from google.appengine.ext import ndb

def topic_key(topic_name=0):
    return ndb.Key('Coach',topic_name)

class Coach(ndb.Model):
    equations = ndb.StringProperty(repeated=true)
    
    