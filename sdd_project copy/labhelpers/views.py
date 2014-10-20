from django.http import HttpResponse    #ADDED THIS
from django.template import RequestContext, loader #ADDED IN 2nd MODIFICATION
from django.shortcuts import render     #ADDED IN 3rd MODIFICATION
from django.http import Http404         #ADDED IN 4th MODIFICATION
from django.shortcuts import get_object_or_404, render #ADDED IN 5TH MODIFICATION
from django.shortcuts import get_object_or_404  #ADDED IN 6TH MODIFICATION
from django.http import HttpResponseRedirect    #ADDED IN 6TH MODIFICATION
from django.core.urlresolvers import reverse    #ADDED IN 6TH MODIFICATION

from labhelpers.models import Question, Answer, Lab, Topic   #ADDED THIS IN 2nd MODIFICATION

#1st MODIFICATION:
#COMMENTED OUT in 2nd MODIFICATION (OVERWRITTEN BELOW)
'''
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
    #call this view from polls/urls.py
'''

#ADDING MORE VIEWS IN 1st MODIFICATION:
'''
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
'''

#4th MODIFICATION -- overwrite def detail()
'''
#The new concept here: The view raises the Http404 exception if a question with the requested ID doesn't exist.
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'question': question})
'''
#5th MODIFICATION
'''
It's a very common idiom to use get() and raise Http404 if the object doesn't exist. 
Django provides a shortcut. Here's the detail() view, rewritten. 

The get_object_or_404() function takes a Django model as its first argument and an 
arbitrary number of keyword arguments, which it passes to the get() function of the model's 
manager. It raises Http404 if the object doesn't exist.

Why do we use a helper function get_object_or_404() instead of automatically catching the 
ObjectDoesNotExist exceptions at a higher level, or having the model API raise Http404 
instead of ObjectDoesNotExist?

Because that would couple the model layer to the view layer. One of the foremost design 
goals of Django is to maintain loose coupling. Some controlled coupling is introduced in 
the django.shortcuts module.

There's also a get_list_or_404() function, which works just as get_object_or_404() 
- except using filter() instead of get(). It raises Http404 if the list is empty.
'''
#8th MODIFICATION -- Comment out existing code and recreate at the bottom of file
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question':question}) 
'''
 
#7th MODIFICATION -- almost the same as "def detail()" view
#now you need to create a template, aka:: .../polls/templates/polls/results.html 
'''
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
'''

#8th MODIFICATION -- Comment out existing code and recreate at the bottom of file
'''
def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''

#6th MODIFICATION -- overwrite dummy votes view with form action
'''
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
'''
'''
request.POST is a dictionary like object that lets you access submitted data by key name.
Here, request.POST['choice'] returns the ID of the selected choice, as a string.

request.POST values are always strings.
request.POST will raise KeyError if choice wasn't provided in POST data. The code checks 
for KeyError and redisplays the question form with an error msg if choice isn't given.

After incrementing the choice count, the code returns HttpResponseRedirect rather than 
HttpResponse. The former takes a single arg, the URL to which the user will be redirected.
* Always use HttpResponseRedirect after successfully dealing with POST data -- it's good
web dev practice.

The reverse() fn in HttpResponseRedirect helps avoid having to hardcode a URL in the view 
fn. It is given the name of the view that we want to pass control to and the variable 
portion of the URL pattern that points to that view.

Here, the reverse() call will return a string like: '/polls/3/results/' , where p.id = 3
The redirected URL will then call the 'results' view to display the final page.

request is an HttpRequest object

After someone votes in a question, the vote() view redirects to the results page for that 
question. See polls/views.py, under def results() 

'''

#8th MODIFICATION -- Comment out existing code and recreate at the bottom of file
'''
def vote(request, question_id):
    p=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {'question': p, 'error_message': "You didn't select a choice",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing with POST data.
        #This prevents data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
'''
#NOW WIRE THESE NEW VIEWS INTO POLLS.URLS.PY MODULE BY ADDINT URL() CALLS

#ABOUT VIEWS
'''
Each view is responsible for doing one of two things: 
1.returning an HttpResponse object containing the content for the requested page, or 
2. raising an exception such as Http404. The rest is up to you.

Your view can read records from a database, or not. 
It can use a template system such as Django's - or a third-party Python template system - or not. 
It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, 
using whatever Python libraries you want.

All Django wants is that HttpResponse. Or an exception.
'''

'''
Because it's convenient, let's use Django's own database API, which we covered in Tutorial 1. 
Here's one stab at a new index() view, which displays the latest 5 poll questions in the system, 
separated by commas, according to publication date:
'''

#1st MODIFICATION (index)
'''
def index(request):
    lastest_question_list = Question.objects.order_by('_pub_date')[:5]
    output = ', '.join([p.question_text for p in latest_question_list])
    return HttpResponse(output)
'''
'''
There's a problem here, though: the page's design is hard-coded in the view. 
If you want to change the way the page looks, you'll have to edit this Python code. 
So let's use Django's template system to separate the design from Python by creating 
a template that the view can use.
'''


#2nd MODIFICATION
'''
This code loads the template in polls/templates/polls/index.html and passes it context.
The context is a dictionary mapping the template variable names to Python objects.

Load the page by pointing your browser at "/polls/", and you should see a bulleted-list 
containing the "What's up" question from Tutorial 1. The link points to the question's detail page.

It's a very common idiom to load a template, fill a context and return an HttpResponse 
object with the result of the rendered template.
'''
'''
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))
'''
    
#3rd MODIFICATION
'''
  - you no longer need to import loader, RequestContext, HttpResponse --unless you still 
  have the stub methods for detail, results, and vote:
  
from django.shortcuts import render

from polls.models import Question
'''
#8th MODIFICATION -- Comment out existing code and recreate at the bottom of file
'''
def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
'''
#ABOUT RENDER(arg1, arg2, arg3)
'''
The render() function takes the request object as its first argument, 
a template name as its second argument and a dictionary as its optional third argument. 
It returns an HttpResponse object of the given template rendered with the given context.
'''

#^----------------------END NON-GENERIC VIEWS ----------------------------^


#8th MODIFICATION
#USE GENERIC VIEWS: Less code is better 
'''
https://docs.djangoproject.com/en/1.7/intro/tutorial04/

The detail() (from Tutorial 3) and results() views are stupidly simple - and, as mentioned 
above, redundant. The index() view (also from Tutorial 3), which displays a list of polls, 
is similar.

These views represent a common case of basic Web development: getting data from the 
database according to a parameter passed in the URL, loading a template and returning the 
rendered template. Because this is so common, Django provides a shortcut, called the 
"generic views" system.

Generic views abstract common patterns to the point where you don't even need to write 
Python code to write an app.

Let's convert our poll app to use the generic views system, so we can delete a bunch of 
our own code. We'll just have to take a few steps to make the conversion. We will:

Convert the URLconf.
Delete some of the old, unneeded views.
Introduce new views based on Django's generic views.

Steps::
Amend polls/urls.py
Amend polls/views.py

'''
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone #ADDED IN 9TH MODIFICATION

from labhelpers.models import Answer, Question, Lab, Topic

#HOMEPAGE VIEW
class HomepageView(generic.ListView):
    template_name='labhelpers/homepage.html'
    context_object_name = 'lab_list' #response.context_data['latest_question_list'] extracts the data this view places into the context.

    def get_queryset(self):
        #Return questions in order of question id
        return Lab.objects.order_by('lab_id')
        #TODO: add above, ".filter(lab_id=____, topic_id=____)" to refine data pulled

    
        
class LabDetailView(generic.DetailView):
    model = Question
    template_name = 'labhelpers/lab_detail.html'
    

    def get_queryset(self):
        #Return questions associated with a particular lab # in order of question id
        return Question.objects.all()   #filter(lab_list.lab_id) #.order_by('question_id')
        #return Question.objects.all().filter(lab_id=lab_id).order_by('question_id')
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'labhelpers/results.html'

def submit(request, question_id):
    p=get_object_or_404(Question, pk=lab_id)   #pk=question_id)
    try:
        selected_answer=p.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question form
        return render(request, 'labhelpers/lab_detail.html', {'question': p, 'error_message': "You didn't select an answer",})
    else:
        selected_answer.submit +=1   #TODO: update this code to reflect if answer was correct
        selected_answer.save()
        #Always return an HttpResponseRedirect after successfully dealing with POST data.
        #This prevents data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('labhelpers:results', args=(p.id,)))

'''
We're using two generic views here: ListView and DetailView. 
Those two views abstract the concepts of "display a list of objects" and 
"display a detail page for a particular type of object."

Each generic view needs to know what model it will be acting upon. 
This is provided using the model attribute.

The DetailView generic view expects the primary key value captured from the URL to be 
called "pk" (as seen in polls/urls.py), so we've changed question_id to pk for the 
generic views.

By default, the DetailView generic view uses a template called: 
<app name>/<model name>_detail.html. Here it would use: 
"polls/question_detail.html". 

The template_name attribute is used to tell Django to use a specific template name instead 
of the autogenerated default template name. 

We also specify the template_name for the results list view - this ensures that the 
results view and the detail view have a different appearance when rendered, even though 
they're both a DetailView behind the scenes.

Similarly, the ListView generic view uses a default template called: 
<app name>/<model name>_list.html; we use template_name to tell ListView to use our existing 
"polls/index.html" template.

In previous parts of the tutorial, the templates have been provided with a context that 
contains the question and latest_question_list context variables. 

For DetailView the question variable is provided automatically - since we're using a 
Django model (Question), Django is able to determine an appropriate name for the context 
variable. 

However, for ListView, the automatically generated context variable is question_list. 
To override this we provide the context_object_name attribute, specifying that we want to 
use latest_question_list instead. 

As an alternative approach, you could change your templates to match the new default 
context variables - but it's a lot easier to just tell Django to use the variable you want.
'''


