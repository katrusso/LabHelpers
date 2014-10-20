'''
When somebody requests a page from your Web site - say, "/polls/34/", Django will load 
the mysite.urls Python module because it's pointed to by the ROOT_URLCONF setting.

It finds the variable named urlpatterns and traverses the regular expressions in order

The idea behind include() is to make it easy to plug-and-play URLs. 
Since polls are in their own URLconf (polls/urls.py), they can be placed under "/polls/", 
or under "/fun_polls/", or under "/content/polls/", or any other path root, and the app will still work.

Here's what happens if a user goes to "/polls/34/" in this system:

Django will find the match at '^polls/'

Then, Django will strip off the matching text ("polls/") and send the remaining 
text - "34/" - to the 'polls.urls' URLconf for further processing which 
matches r'^(?P<question_id>\d+)/$' resulting in a call to the detail() view like so:

detail(request=<HttpRequest object>, question_id='34')

The question_id='34' part comes from (?P<question_id>\d+). 

'''

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^labhelpers/', include('labhelpers.urls', namespace="labhelpers")), #ADDED THIS TO THE FILE, makes url: http://localhost:8000/polls/
    url(r'^admin/', include(admin.site.urls)), #makes url: http://localhost:8000/admin/
)

'''
Namespacing URL names
The tutorial project has just one app, polls. In real Django projects, there might be 
five, ten, twenty apps or more. How does Django differentiate the URL names between them? 

For example, the polls app has a detail view, and so might an app on the same project that 
is for a blog. How does one make it so that Django knows which app view to create for 
a url when using the {% url %} template tag?

The answer is to add namespaces to your root URLconf. 
In the mysite/urls.py file, go ahead and change it to include namespacing:
'''

'''
url() is passed 4 args: 2 req'd, 2 optional:
    regex, view
    kwargs, name
    
regex: regular expression
 - a syntax for matching patterns in strings or url patterns
 - Django starts at the first reg. expression and makes its way down the list, 
 comparing the requested URL against each regular expression until it finds one that matches
  - NOTE: reg expressions do NOT search GET or POST parameters, or the domain name
  e.g. http://www.example.com/myapp/
  the URLconf will look for myapp/

view: 
 - when Django finds an expression match, it calls the specified view fn with an HttpRequest
 object as the first arg and any "captured" values from the expression as other args.
 - if regex uses simple captures, values are passed as positional arguments;
 - if it uses named captures, values are passed as keyword args
 
 kwargs:
 - arbitrary keyword args can be passed in a dict to the target view
 
 name:
 - naming your url lets you refer to it unambiguously from elsewhere in django
 - this feature allows you to make global changes to the url patterns of your project using a single file.
'''