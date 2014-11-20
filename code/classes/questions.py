from google.appengine.ext import ndb                    #GOOGLE APP ENGINE DATASTORE
import topic

def lab_key(labid=0):                                   #KEY ASSOCIATED WITH STATIC LAB ID  
    return ndb.Key('Labs', labid)       

def lab_key_topic(topic):                               #KEY ASSOCIATED WITH DYNAMIC LAB ID 
    return ndb.Key('Labs',4444)

class Question(ndb.Model):                              #QUESTION MODEL AND ITS RESPECTIVE ATTRIBUTES
    number = ndb.IntegerProperty()                      #QUESTION NUMBER (FOR ORDERING PURPOSES)
    topic = ndb.StringProperty()                        #TOPIC ASSOCIATED WITH QUESTION
    question = ndb.StringProperty()                     #QUESTION TEXT
    choices = ndb.StringProperty(repeated=True)         #MULTIPLE CHOICE OPTIONS
    answers = ndb.IntegerProperty(repeated=True)        #CORRECT ANSWER(S)
