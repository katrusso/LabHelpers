from google.appengine.ext import ndb

def topic_key(topic_name):
    return ndb.Key('Coach',topic_name)

class Coach(ndb.Model):
    equations = ndb.StringProperty(repeated=True)
    summary = ndb.StringProperty()
    example = ndb.StringProperty()
    
