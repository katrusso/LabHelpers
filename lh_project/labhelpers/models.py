import datetime

from django.db import models
from django.utils import timezone



#STUDENTS
class User(models.Model):
    user_name=models.CharField(max_length=50)   
    user_rin=models.IntegerField()      
    
    def __str__(self):
        return self.user_name             

#LAB NAME & ID
class Lab(models.Model):
    lab_id = models.IntegerField()
    lab_name = models.CharField(max_length=200)
    lab_type = models.CharField(max_length=8, default='STATIC')
   
    
    def __str__(self):
        return self.lab_name


#TOPICS (FOR QUESTIONS)
class Topic(models.Model):
    lab=models.ManyToManyField("self")  #changed from foreign key for lab class
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=200)
    coach_data = models.TextField()
    
    def __str__(self):
        return self.topic_name


    
#LAB QUESTIONS
class Question(models.Model):
    lab = models.ForeignKey(Lab)    #each question is paired with a particular lab
    #topic = models.ManyToManyField("self")
    topic = models.ForeignKey(Topic)
    question_id = models.IntegerField()
    question_text = models.TextField()
    #TODO: add question image
    question_hint = models.TextField()
    
    def __str__(self):
        return self.question_text
    
#LAB ANSWERS
class Answer(models.Model):
    question = models.ForeignKey(Question)  #each answer is paired with a particular question
    correct_answer_text = models.CharField(max_length=200)
    wrong_answer_text_1 = models.CharField(max_length=200, default='')
    wrong_answer_text_2 = models.CharField(max_length=200, default='')
    wrong_answer_text_3 = models.CharField(max_length=200, default='')
    wrong_answer_text_4 = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.correct_answer_text




#1st MODIFICATION
#    def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#    was_published_recently.admin_order_field = 'pub_date'
#    was_published_recently.boolean = True
#    was_published_recently.short_description = 'Published recently?'