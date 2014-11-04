import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *


MAXCOMMENT = 9
DEFAULT_GUESTBOOK_NAME = 'General Comments'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

#database class for a message
class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

#webpage for the comments 
class CommentPage(webapp2.RequestHandler):
  def get(self):
        self.response.write(OPEN_HTML.substitute(head='''<link type="
        text/css" rel="stylesheet" href="/stylesheets/comment.css" 
            />'''))
        self.response.write('''<div class="header">''')
        self.response.write('<h1> <img src="stylesheets/emc24.png" alt="E=mc^2 image" width="40px" height="25px"> Lab Helpers </h1>')
        self.response.write('</div>')#header
        
        self.response.write('''<div class="sub-heading">''')
        self.response.write('<h2>Let us know how we\'re doing <br><br></h2>')
        self.response.write('</div>')#sub-heading
        
        
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(MAXCOMMENT)
        greetings.reverse()
        #write previous comments
        self.response.write('''<div class="comment-body">''')
        for greeting in greetings:
            if greeting.author:
            	self.response.write('<h3><b>%s</b> wrote:<br></h3>' % greeting.author.nickname())
                #self.response.write(
                 #       '<b>%s</b> wrote:' % greeting.author.nickname())
            else:
            	self.response.write('<h3>An anonymous person wrote:<br></h3>')
                #self.response.write('An anonymous person wrote:')
            self.response.write('<h4><blockquote>%s</blockquote></h4>' %
                                cgi.escape(greeting.content))
            self.response.write('</div>')#comment-body
            
            #self.response.write('<blockquote>%s</blockquote>' %
             #                   cgi.escape(greeting.content))

        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})
        self.response.write(FORM_HTML.substitute(
            action="/sign?%s" % (sign_query_params),
            method="post"))
        self.response.write(TEXTBOX_HTML.substitute(name="content",
                                                    row=3,
                                                    col=60,
                                                    text=""))
        self.response.write(SUBMIT_HTML.substitute(value="Leave Comment"))
        self.response.write(CLOSE_FORM_HTML)
        self.response.write(LINK_HTML.substitute(link="/", 
                                                 text="Return to Main Page"))

#submit the comment to the database
class Comment(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/comment?' + urllib.urlencode(query_params))



        
