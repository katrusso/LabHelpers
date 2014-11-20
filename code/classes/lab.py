from google.appengine.ext import ndb                #GOOGLE APP ENGINE DATASTORE

def lab_key(lab_id=0):                              #KEY ASSOCIATED WITH LAB ID
    return ndb.Key('LabClasses',lab_id)

class Lab(ndb.Model):                               #LAB MODEL AND ITS RESPECTIVE ATTRIBUTES
    name = ndb.StringProperty()                     #LAB NAME
    id = ndb.IntegerProperty()                      #LAB ID
