from google.appengine.ext import ndb                #GOOGLE APP ENGINE DATASTORE

def topic_key(topic_name):                          #KEY ASSOCIATED WITH COACH TOPIC
    return ndb.Key('Coach',topic_name)

class Coach(ndb.Model):                             #COACH MODEL AND ITS RESPECTIVE ATTRIBUTES
    equations = ndb.StringProperty(repeated=True)   #RELATED EQUATIONS TO THE TOPIC
    summary = ndb.StringProperty()                  #SUMMARY/EXPLANATION OF THE TOPIC
    example = ndb.StringProperty()                  #EXAMPLE TO CLARIFY EXPLANATION
    
