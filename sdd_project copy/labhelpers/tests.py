import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse #ADDED IN 3rd MODIFICATION
from polls.models import Question

class QuestionMethodTests(TestCase):
    #1st MODIFICATION
    def test_was_published_recently_with_future_question(self):
        #was_published_recently() should return False for questions whose pub_date is in the future

        time=timezone.now() + datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)
    
'''
This creates a "django.test.TestCase" subclass with a method that creates a Question 
instance with a pub_date in the future.

We check the output of "was_published_recently()", which ought to be False

To run:
$ python manage.py test polls
'''

#1st MODIFICATION OUTPUT
'''
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionMethodTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/path/to/mysite/polls/tests.py", line 16, in test_was_published_recently_with_future_question
    self.assertEqual(future_question.was_published_recently(), False)
AssertionError: True != False

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...
'''

#EXPLANATION:
'''
python manage.py test polls looked for tests in the polls application

it found a subclass of the django.test.TestCase class

it created a special database for the purpose of testing

it looked for test methods - ones whose names begin with test

in test_was_published_recently_with_future_question it created a Question instance whose 
pub_date field is 30 days in the future

using the assertEqual() method, it discovered that its was_published_recently() returns 
True, though we wanted it to return False

The test informs us which test failed and even the line on which the failure occurred.

TO FIX:
Question.was_published_recently() should return False if its pub_date is in the future. 
Amend the method in models.py, so that it will only return True if the date is also in the past.
'''

#2nd MODIFICATION -- adding additional tests

def test_was_published_recently_with_old_question(self):
    #was_published_recently() should return False for questions whose
    #pub_date is older than 1 day
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(pub_date=time)
    self.assertEqual(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        #was_published_recently() should return True for questions whose
        #pub_date is within the last day
        
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)
        
'''
now we have three tests that confirm that Question.was_published_recently() returns 
sensible values for past, recent, and future questions.
'''

#3rd MODIFICATION -- ADD A SHORTCUT FN TO CREATE Qs AS WELL AS A NEW TEST CLASS.
#Creates a Q with the given question_text published the given number of days
#offset to now (negative for Qs published in the past, positive for Qs yet to be published


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        
'''
First is a question shortcut function, create_question, to take some repetition out of 
the process of creating questions.

test_index_view_with_no_questions doesn't create any questions, but checks the message: 
"No polls are available." and verifies the latest_question_list is empty. Note that the 
django.test.TestCase class provides some additional assertion methods. 

In these examples, we use assertContains() and assertQuerysetEqual().

In test_index_view_with_a_past_question, we create a question and verify that it appears 
in the list.

In test_index_view_with_a_future_question, we create a question with a pub_date in the 
future. The database is reset for each test method, so the first question is no longer 
there, and so again the index shouldn't have any questions in it.

And so on. In effect, we are using the tests to tell a story of admin input and user 
experience on the site, and checking that at every state and for every new change in the 
state of the system, the expected results are published.

What we have works well; however, even though future questions don't appear in the index, 
users can still reach them if they know or guess the right URL. So we need to add a similar 
constraint to DetailView (polls/views.py)
'''

#4th MODIFICATION
#add some tests, to check that a Question whose pub_date is in the past can be displayed, 
#and that one with a pub_date in the future is not:

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        response = self.client.get(reverse('polls:detail',
                                   args=(past_question.id,)))
        self.assertContains(response, past_question.question_text,
                            status_code=200)
                            
'''
Ideas for more tests
We ought to add a similar get_queryset method to ResultsView and create a new test class 
for that view. It'll be very similar to what we have just created; in fact there will be a 
lot of repetition.

We could also improve our application in other ways, adding tests along the way. 
For example, it's silly that Questions can be published on the site that have no Choices. 
So, our views could check for this, and exclude such Questions. Our tests would create a 
Question without Choices and then test that it's not published, as well as create a 
similar Question with Choices, and test that it is published.

Perhaps logged-in admin users should be allowed to see unpublished Questions, but not 
ordinary visitors. Again: whatever needs to be added to the software to accomplish this 
should be accompanied by a test, whether you write the test first and then make the code 
pass the test, or work out the logic in your code first and then write a test to prove it.

At a certain point you are bound to look at your tests and wonder whether your code is 
suffering from test bloat, which brings us to:

When testing, more is better
It might seem that our tests are growing out of control. At this rate there will soon 
be more code in our tests than in our application, and the repetition is unaesthetic, 
compared to the elegant conciseness of the rest of our code.

It doesn't matter. Let them grow. For the most part, you can write a test once and then 
forget about it. It will continue performing its useful function as you continue to 
develop your program.

Sometimes tests will need to be updated. Suppose that we amend our views so that only 
Questions with Choices are published. In that case, many of our existing tests will 
fail - telling us exactly which tests need to be amended to bring them up to date, so 
to that extent tests help look after themselves.

At worst, as you continue developing, you might find that you have some tests that are 
now redundant. Even that's not a problem; in testing redundancy is a good thing.

As long as your tests are sensibly arranged, they won't become unmanageable. Good 
rules-of-thumb include having:

a separate TestClass for each model or view
a separate test method for each set of conditions you want to test
test method names that describe their function
Further testing
This tutorial only introduces some of the basics of testing. There's a great deal more 
you can do, and a number of very useful tools at your disposal to achieve some very clever 
things.

For example, while our tests here have covered some of the internal logic of a model 
and the way our views publish information, you can use an "in-browser" framework such as 
Selenium to test the way your HTML actually renders in a browser. These tools allow you 
to check not just the behavior of your Django code, but also, for example, of your 
JavaScript. It's quite something to see the tests launch a browser, and start interacting 
with your site, as if a human being were driving it! Django includes LiveServerTestCase 
to facilitate integration with tools like Selenium. 

If you have a complex application, you may want to run tests automatically with every 
commit for the purposes of continuous integration, so that quality control is itself - at 
least partially - automated.

A good way to spot untested parts of your application is to check code coverage. 
This also helps identify fragile or even dead code. If you can't test a piece of code, 
it usually means that code should be refactored or removed. Coverage will help to 
identify dead code. See Integration with coverage.py for details.

Testing in Django has comprehensive information about testing.

FULL DETAILS ON TESTING IN DJANGO:
https://docs.djangoproject.com/en/1.7/topics/testing/

'''