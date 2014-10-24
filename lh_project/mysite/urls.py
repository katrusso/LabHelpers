from django.conf.urls import patterns, include, url
from django.contrib import admin
#admin.autodiscover()   #PYTHON-GETTING-STARTED

urlpatterns = patterns('',
    url(r'^labhelpers/', include('labhelpers.urls', namespace="labhelpers")),   #makes url: http://localhost:8000/labhelpers/
    url(r'^admin/', include(admin.site.urls)),                                  #makes url: http://localhost:8000/admin/
)


#import hello.views
#    url(r'^$', hello.views.index, name='index'),
#    url(r'^db', hello.views.db, name='db'),
#    url(r'^admin/', include(admin.site.urls)),