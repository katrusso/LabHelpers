from google.appengine.ext import ndb                                    #GOOGLE APP ENGINE DATASTORE

def sign_in(page, nickname):
    user_query = User.query(
        ancestor=user_key(nickname)).order(
            User.rin_number)
    user_object = user_query.fetch()
    if (len(user_object)==0):
        page.redirect("/signup")
    return user_object


def user_key(username):                                                 #USER KEY ASSOCIATED WITH USERNAME
    return ndb.Key('User',username)

def lab_response_key(lab_id,username):                                  #LAB RESPONSE KEY ASSOCIATED WITH USERNAME AND LAB ID
    return ndb.Key('Responses',lab_id,'user',username)

class LabResponses(ndb.Model):                                          #LAB RESPONSES MODEL AND ITS RESPECTIVE ATTRIBUTES
    responses = ndb.IntegerProperty(repeated=True)                      #USER RESPONSES
    correct = ndb.IntegerProperty(repeated=True)                        #CORRECT RESPONSES

class User(ndb.Model):                                                  #USER MODEL AND ITS RESPECTIVE ATTRIBUTES
    def __query_responses__(self,lab_id,username):                      #GET USER RESPONSES FROM DATASTORE
        lab_responses = LabResponses.query(
            ancestor=lab_response_key(lab_id,username))
        return lab_responses.fetch()
    
    def __add_responses__(self,lab_id,username,responses,correct):      #SAVE USER RESPONSES TO DATASTORE
        lab_responses = LabResponses(
            parent=lab_response_key(lab_id,username))
        lab_responses.responses=responses
        lab_responses.correct=correct
        lab_responses.put()

    rin_number = ndb.StringProperty()                                   #USER RIN NUMBER
    lab_ids = ndb.IntegerProperty(repeated=True)                        #LAB IDS ASSOCIATED WITH USER
    
