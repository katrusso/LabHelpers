from google.appengine.ext import ndb                    #GOOGLE APP ENGINE DATASTORE

def topic_key(topic_id=0):                              #KEY ASSOCIATED WITH LAB ID
    return ndb.Key('Topic',topic_id)

class Topic(ndb.Model):                                 #TOPIC MODEL AND ITS RESPECTIVE ATTRIBUTES
    name = ndb.StringProperty()                         #TOPIC NAME
    
