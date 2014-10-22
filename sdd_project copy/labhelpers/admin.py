from django.contrib import admin
from labhelpers.models import Question, Answer, Lab, Topic, User


#ADMIN - ANSWERS TABLE
#class AnswerInline(admin.StackedInline):   #stacked format (takes up more space)
class AnswerInline(admin.TabularInline):    #tabular format
    model=Answer
    extra=1        #creates 4 choice input fields to correspond with one question



#ADMIN - TOPICS TABLE
class TopicAdmin(admin.ModelAdmin):  #includes question fields
    fieldsets = [
        (None,                  {'fields':['topic_id', 'topic_name', 'coach_data']}),
        #('Date information',    {'fields':['pub_date'], 'classes': ['collapse']}), #default: date info collapsed
    ]
    #inlines = [AnswerInline] #this tells django "answer" objects are edited in the question admin page
    list_display = ('topic_id', 'topic_name', 'coach_data') #creates columns with these headings in the all-questions section
    list_filter = ['topic_id']  #adds a date filter in the right margin
    search_fields = ['topic_name'] #adds a field that lets you search by words in a question
    
admin.site.register(Topic, TopicAdmin)



#ADMIN - QUESTIONS TABLE
class QuestionAdmin(admin.ModelAdmin):  #includes question fields
    fieldsets = [
        (None,                  {'fields':['lab','topic','question_id', 'question_text','question_hint']}),
        #('Date information',    {'fields':['pub_date'], 'classes': ['collapse']}), #default: date info collapsed
    ]
    inlines = [AnswerInline] #this tells django "answer" objects are edited in the question admin page
    list_display = ('lab','topic', 'question_id','lab','question_text', 'question_hint') #creates columns with these headings in the all-questions section
    list_filter = ['lab_id']  #adds a date filter in the right margin
    search_fields = ['question_text'] #adds a field that lets you search by words in a question
    
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Answer)



#ADMIN - LABS TABLE
class LabAdmin(admin.ModelAdmin):  #includes question fields
    fieldsets = [
        (None,                  {'fields':['lab_id', 'lab_name', 'lab_type']}),
        #('Date information',    {'fields':['pub_date'], 'classes': ['collapse']}), #default: date info collapsed
    ]
    #inlines = [AnswerInline] #this tells django "answer" objects are edited in the question admin page
    list_display = ('lab_id', 'lab_name', 'lab_type') #creates columns with these headings in the all-questions section
    list_filter = ['lab_id']  #adds a date filter in the right margin
    search_fields = ['lab_name'] #adds a field that lets you search by words in a question
    
admin.site.register(Lab, LabAdmin)


