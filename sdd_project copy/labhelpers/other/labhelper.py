#helloworld 2
#Users service: lets your app integrate with Google user accounts
#users can use the google accounts they already have to sign in to your app

#When your app is running on App Engine, users will be directed to the Google Accounts sign-in page 
#then redirected back to your app after successfully signing in or creating an account.

from google.appengine.api import users

import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
	        # Checks for active Google account session
    	    #If the user is already signed into the app, get_current_user() returns the user object, else returns none.
        user = users.get_current_user()

			#if the user has signed in, display a personalized msg using the nickname associated with their account
			#else, redirect to google's account sign-in screen
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)