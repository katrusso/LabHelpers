from google.appengine.ext import ndb

def __sign_in__(page, nickname):
    user_query = User.query(
        ancestor=user_key(nickname)).order(
            User.rin_number)
    user_object = user_query.fetch()
    if (len(user_object)==0):
        page.redirect("/signup")
    return user_object


def user_key(username):
    return ndb.Key('User',username)

def lab_response_key(lab_id,username):
    return ndb.Key('Responses',lab_id,'user',username)

class LabResponses(ndb.Model):
    responses = ndb.IntegerProperty(repeated=True)

class User(ndb.Model):
    def query_responses(self,lab_id,username):
        responses = LabResponses.query(
            ancestor=lab_response_key(lab_id,username))
        return responses.fetch()

    rin_number = ndb.StringProperty()
    lab_ids = ndb.IntegerProperty(repeated=True)
    
