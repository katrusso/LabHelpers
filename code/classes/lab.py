
from google.appengine.ext import ndb

def lab_key(lab_id=0):
    return ndb.Key('LabClasses',lab_id)

class Lab(ndb.Model):
    name = ndb.StringProperty()
