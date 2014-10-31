import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from html_constants import *

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Leave Comment"></div>
    </form>
    <hr>
"""

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
        self.response.write(OPEN_HTML.substitute(head=""))
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(MAXCOMMENT)

        #write previous comments
        for greeting in greetings:
            if greeting.author:
                self.response.write(
                        '<b>%s</b> wrote:' % greeting.author.nickname())
            else:
                self.response.write('An anonymous person wrote:')
            self.response.write('<blockquote>%s</blockquote>' %
                                cgi.escape(greeting.content))

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
        self.response.write(FORM_HTML.substitute(action="/", method="link"))
        self.response.write(SUBMIT_HTML.substitute(value="Return to Main Page"))
        self.response.write(CLOSE_FORM_HTML)

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



        
