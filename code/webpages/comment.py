import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2                                                                      #FRAMEWORK
from html_constants import *                                                        #REDUCES CODE REDUNDANCY ACROSS FILES


MAXCOMMENT = 9
DEFAULT_GUESTBOOK_NAME = 'General Comments'

'''
OUR COMMENTS PAGE IS REFERENCED HERE AS GUESTBOOK. 

WE SET A PARENT KEY ON THE 'GREETINGS' TO ENSURE THAT THEY ARE ALL IN THE SAME ENTITY 
GROUP. QUERIES ACROSS THE SINGLE ENTITY GROUP WILL BE CONSISTENT. HOWEVER, THE WRITE 
RATE SHOULD BE LIMITED TO ~1/SECOND.

THE METHODS BELOW RETRIEVE THE USER NAME, CONTENT OF THEIR COMMENT, AND DATE OF SUBMISSION; 
ALL STORED IN OUR DATASTORE. THE COMMENTPAGE METHOD RETRIEVES THESE MESSAGES AND POSTS 
THEM TO THE COMMENTS WEBPAGE. 

AS A GREETING GETS SUBMITTED (POST METHOD OF CLASS COMMENT), ITS DATA IS SENT TO THE 
DATASTORE, WHERE IT IS THEN RETRIEVED AND DISPLAYED ON THE WEBPAGE.
'''


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)                                     #CONSTRUCTS A DATASTORE KEY FOR A GUESTBOOK ENTITY WITH GUESTBOOK_NAME


class Greeting(ndb.Model):                                                          #DATABASE CLASS FOR A MESSAGE; MODELS AN INDIVIDUAL GUESTBOOK ENTRY       
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

 
class CommentPage(webapp2.RequestHandler):                                          #GENERATES A WEBPAGE FOR THE COMMENTS AND POSTS THEM
  def get(self):
        self.response.write(OPEN_HTML.substitute(head='''<link 
        rel="stylesheet" href="/stylesheets/comment.css" />'''))                    #STYLESHEET - MAIN
        
        write_css_html(self,"Let us know how we're doing")                          #SUBHEADING
        
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(                                           #FETCH (PREVIOUS) COMMENTS / AUTHOR DATA FROM DATASTORE AND POST ON WEBPAGE BY DATE IN DESCENDING ORDER
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(MAXCOMMENT)
        greetings.reverse()
        self.response.write(CSS_CLASS_HTML.substitute(id="comment-body"))           #STYLESHEET - OPEN TAG :: COMMENT-BODY
        for greeting in greetings:
            if greeting.author:
            	self.response.write('<h3><b>%s</b> wrote:<br></h3>' % greeting.author.nickname())
            else:
            	self.response.write('<h3>An anonymous person wrote:<br></h3>')
            self.response.write('<h4><blockquote>%s</blockquote></h4>' %
                                cgi.escape(greeting.content))
        self.response.write(CLOSE_CSS_HTML)                                         #STYLESHEET - CLOSING TAG :: COMMENT-BODY
    
        
        sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})    #CREATE THE SUBMISSION FORM (INPUT BOX WHERE USERS KEY IN COMMENTS) 
        self.response.write(FORM_HTML.substitute(
            action="/sign?%s" % (sign_query_params),
            method="post"))
        self.response.write(TEXTBOX_HTML.substitute(name="content",
                                                    row=3,
                                                    col=60,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Leave Comment"))          #BUTTON: "LEAVE COMMENT" TO POST COMMENT
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(LINK_HTML.substitute(link="/", 
                                                 text="Return to Main Page"))
        self.response.write(CLOSE_HTML)                                             #END SUBMISSION FORM

class Comment(webapp2.RequestHandler):                                              #SUBMIT THE COMMENT TO THE DATABASE
    def post(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/comment?' + urllib.urlencode(query_params))



        
