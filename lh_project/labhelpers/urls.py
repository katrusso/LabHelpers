#URLconf

#to call a view (in views.py), we need to map it to a URL
from django.conf.urls import patterns, url


from labhelpers import views


urlpatterns = patterns('',
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^(?P<pk>\d+)/$', views.LabDetailView.as_view(), name='lab_detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>\d+)/submit/$', views.submit, name='submit'),
)

#2nd MODIFICATION -- USING GENERIC VIEWS
'''
Note: the name of the matched pattern in the regexes of the 2nd and 3rd patterns has 
changed from <question_id> to <pk> (stands for primary key).
'''

#NEXT: delete some old, unneeded views (index, detail, results) in polls/views.py.

#1st MODIFICATION -- USING NON-GENERIC VIEWS
'''
#--ADDED NEW VIEWS IN views.py -- need to add url() calls:
urlpatterns = patterns('', 
    #ex: /polls/
    url(r'^$', views.index, name='index'), 
    #ex: /polls/5/  #calls the detail view (views.detail) and passes in anything after "polls/" -- so 5 is read as the question_id
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    #ex: /polls/5/results/  #using () around a pattern capture the text matched by that pattern and sends it as a arg to the view fn (in this case, the question_id gets passed as text)
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    #ex: /polls/5/vote/ #\d+ is a regex to match a sequence of digits (i.e. a number)
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)
'''

'''
If you want to change the URL of the polls detail view to something else, perhaps to 
something like polls/specifics/12/ instead of doing it in the template (or templates) you 
would change it in polls/urls.py:

...
# added the word 'specifics'
url(r'^specifics/(?P<question_id>\d+)/$', views.detail, name='detail'),
...
'''
#NOW, POINT THE ROOT URLconf AT THE polls.urls.py MODULE BY EDITING mysite/urls.py

