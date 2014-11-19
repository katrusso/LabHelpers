import os
import urllib
import cgi
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2                                                                      #FRAMEWORK
import questions                                                                    #RELEVANT CLASS
import userclass                                                                    #RELEVANT CLASS
from html_constants import *                                                        #REDUCES CODE REDUNDANCY ACROSS FILES

class LabPage(webapp2.RequestHandler):
     
     
    def get(self):                                                                  #POPULATES LAB DATA
        '''
        THIS METHOD POPULATES THE USER-SELECTED LAB (SELECTED VIA HOMEPAGE LAB-LINK) WITH 
        ITS RESPECTIVE CONTENTS. IF THE USER COMPLETED THE LAB DURING A PREVIOUS VISIT TO
        THE SITE, HIS OR HER ANSWERS ARE SAVED, AND THEREFORE THE CORRECT 
        (POST-SUBMISSION) LAB VERSION APPEARS. 

        IF THE LAB HAS NOT BEEN COMPLETED, ITS QUESTIONS AND MULTIPLE CHOICE OPTIONS
        ARE DISPLAYED IN A FORM FOR THE USER.

        THE PAGE STYLE IS DETERMINED BY ITS ASSOCIATED STYLE SHEET.
        '''          
        self.response.write(OPEN_HTML.substitute(head='''<link 
         rel="stylesheet" href="/stylesheets/labpage.css" />'''))                   #STYLESHEET - MAIN
        
        self.__write_header__()

        self.response.write(FORM_HTML.substitute(action="",method="post"))          #CREATE HTML FORM
        
        self.num=0                                                                      
        user_object =self.__check_login__()                                         #RETRIEVE USER 
        lab_responses=self.__get_responses__(user_object)                           #RETRIEVE USER DATA ASSOCIATED WITH THIS LAB
        self.__gather_questions__(False)
        
        
        if len(lab_responses)!=0 and len(lab_responses[0].responses)==len(self.question_list):
            self.post()                                                             #FOR LAB COMPLETED PRIOR, DISPLAY USER'S CORRECTED-LAB
            return
        if len(self.question_list)==0:                                              
            self.response.write("Sorry no questions to display<br>")
            self.response.write(LINK_HTML.substitute(link="/",
                                text="Return to Main Page"))
            return;
        
        
        self.response.write(CSS_CLASS_HTML.substitute(id="question-body"))           #STYLESHEET CLASS - OPEN TAG :: QUESTION-BODY
        for question in self.question_list:
            self.response.write(CSS_CLASS_HTML.substitute(id="question"))            #STYLESHEET CLASS - OPEN TAG :: QUESTION
            self.num=self.num+1
            self.response.write(str(self.num)+". ")
            self.response.write(question.question)                                   #FOR LAB NOT COMPLETED PRIOR, DISPLAY MULTIPLE CHOICE QUESTIONS/CHOICES
            self.response.write('''<br style="color:black">''')
            for i in range(len(question.choices)):
                ans="wrong"
                if i+1 in question.answers:
                    ans="correct"
                self.response.write(RADIO_HTML.substitute(name="q"+str(self.num),   
                                                          checked="",
                                                          value=str(i)+ans,
                                                          text=question.choices[i])) 
            self.response.write("<br>")
            self.response.write(CLOSE_CSS_HTML)                                     #STYLESHEET CLASS - CLOSING TAG :: QUESTION
        self.response.write(CLOSE_CSS_HTML)                                         #STYLESHEET CLASS - CLOSING TAG :: QUESTION-BODY
        self.response.write(SUBMIT_HTML.substitute(value="Submit"))                 #SUBMIT BUTTON


        self.response.write(CLOSE_FORM_HTML)                                        #END OF FORM
        self.response.write(CLOSE_HTML)                                             #END OF PAGE
    
    
    
   
    def post(self):                                                                 #POPULATES CORRECTED LAB AFTER USER SUBMISSION
        '''
        This method populates the corrected lab data after the user hits the "Submit" 
        button in the above def get(self) method. 
        
        The student can then scroll 
        to the bottom of the page and click a button to generate custom practice problems 
        based on areas of difficulty.
        

        
        The page style is determined by its associated style sheet.

        '''                                                                 
        self.response.write(OPEN_HTML.substitute(head='''<link                  
        rel="stylesheet" href="/stylesheets/labpage.css" />'''))                    #STYLESHEET - MAIN
        
        self.__write_header__()
        
        lab_name = self.__get_lab_name__()                                          
        lab_id = self.__get_labID__()
        user_object =self.__check_login__()                                         #RETRIEVE USER
        self.__gather_questions__(True)                                             #RETRIEVE QUESTIONS
        topics = []
        totals = []
        select = []
        correct = []
        correct_answers=[]
        is_add=True
        
        lab_responses = self.__get_responses__(user_object)                         #RETRIEVE USER RESPONSES
        if len(lab_responses)==0 or len(lab_responses[0].responses)<len(self.question_list):
            for i in range(len(self.question_list)):                                #CHECK TO SEE IF USER RESPONSES ARE CORRECT
                j=0                                                                 #APPEND CORRECT ANSWERS TO DATA STRUCTURE FOR GRADING PURPOSES
                for j in range(len(topics)+1):
                    if j==len(topics) or topics[j]==self.question_list[i].topic:
                        break
                        
                if j>=len(topics):
                    topics.append(self.question_list[i].topic)
                    totals.append(1)
                    correct.append(0)
                else:
                    totals[j]=totals[j]+1
                answer = self.request.get("q"+str(i+1))
                if answer!="":
                    select.append(int(answer[0]))
                else:
                    select.append(-1)
                if answer[1:]=="correct":
                    correct[j] = correct[j]+1
                    correct_answers.append(True)
                else:
                    correct_answers.append(False)
        else:
            is_add=False
            for i in range(len(self.question_list)):
                j=0
                for j in range(len(topics)+1):
                    if j==len(topics) or topics[j]==self.question_list[i].topic:
                        break
                if j>=len(topics):
                    topics.append(self.question_list[i].topic)
                    totals.append(1)
                    correct.append(0)
                else:
                    totals[j]=totals[j]+1
                select.append(lab_responses[0].responses[i])
                correct_answers.append(lab_responses[0].correct[i])
                if lab_responses[0].correct[i]:
                    correct[j]=correct[j]+1
                
      
        num_correct=0                                                               #PRINT THE GRADING RESULTS IN A DASHBOARD AT THE TOP OF THE CORRECTED LAB
        self.response.write(ALIGN_HTML.substitute(align="center"))
        if lab_id==4444:                                                            #LAB_ID 4444 REFERS TO CUSTOM-GENERATED ("DYNAMIC") LAB -- AKA CUSTOM PRACTICE PROBLEMS
            self.response.write("<b><ins> Practice Lab Results </ins></b><br>")
        else:
            self.response.write("<b><ins>Lab "+str(lab_id)+" Results</ins></b><br>")
        self.response.write(OPEN_TABLE_HTML.substitute(percent=50))
        self.response.write("<tr>")
        
        
        for i in topics:                                                            #USER IS GRADED BY TOPIC; HELPS PINPOINT PROBLEM AREAS AND CONCENTRATE PRACTICE PROBLEMS THERE
            self.response.write(TABLE_COLUMN_HTML.substitute(
                text=LINK_HTML.substitute(link=i, text=i)))                         #DASHBOARD IS DISPLAYED IN TABLE FORMAT
        self.response.write(TABLE_COLUMN_HTML.substitute(text="Total")) 
        self.response.write("</tr>")
        self.response.write("<tr>")
        for i in range(len(topics)):
            temp_val = correct[i]*100.0/totals[i]                                   #GRADE CALCULATED: NUM CORRECT IN SECTION/ TOTAL QUESTIONS IN SECTION   (AGAIN, GRADES ARE BROKEN DOWN BY TOPIC)
            num_correct = num_correct + correct[i]
            self.response.write(TABLE_COLUMN_HTML.substitute(
                text = str("{:10.2f}".format(temp_val))+"%"))
        self.response.write(TABLE_COLUMN_HTML.substitute(text = str("{:10.2f}".format(num_correct*100.0/len(self.question_list)))+"%"))
        self.response.write("</tr>")
        self.response.write(CLOSE_TABLE_HTML)
        self.response.write(CLOSE_ALIGN_HTML)                                       #END OF GRADING DASHBOARD TABLE


        self.response.write(CSS_CLASS_HTML.substitute(id="question-body"))          #STYLESHEET CLASS - OPEN TAG :: QUESTION-BODY
        num=0
        for j in range(len(self.question_list)):                                    #POPULATES CORRECTED LAB WITH ORIGINAL QUESTIONS, (REFORMATTED) USER RESPONSES AND CORRECT ANSWERS (FOR VISUAL EMPHASIS)
            self.response.write(CSS_CLASS_HTML.substitute(id="question"))           #STYLESHEET CLASS - OPEN TAG :: QUESTION
            question = self.question_list[j]
            num=num+1
            self.response.write(CSS_CLASS_HTML.substitute(id="section-heading"))    #STYLESHEET CLASS - OPEN TAG :: SECTION-HEADING
            self.response.write(question.topic+"<br>")
            self.response.write(CLOSE_CSS_HTML)                                     #STYLESHEET CLASS - CLOSING TAG :: SECTION-HEADING                                     
            self.response.write(str(num)+". ")
            self.response.write(question.question)
            self.response.write("<br>")
            for i in range(len(question.choices)):
                if select[j]==i and i+1 in question.answers:
                    self.response.write(CSS_CLASS_HTML.substitute(id="correct"))    #STYLESHEET CLASS - OPEN TAG :: CORRECT (IF STMT)      
                elif select[j]==i:                                                  #REFORMAT USER-SELECTED ANSWER IF IT DOESN'T MATCH THE CORRECT ANSWER
                    self.response.write(CSS_CLASS_HTML.substitute(id="incorrect"))  #STYLESHEET CLASS - OPEN TAG :: INCORRECT (IF STMT)  
                elif i+1 in question.answers:
                    self.response.write(CSS_CLASS_HTML.substitute(id="answer"))     #STYLESHEET CLASS - OPEN TAG :: ANSWER (IF STMT)
                self.response.write(TAB_HTML)
                self.response.write(question.choices[i])
                self.response.write("<br>")
                if select[j]==i or i+1 in question.answers:
                    self.response.write(CLOSE_CSS_HTML)                             #STYLESHEET CLASS - CLOSING TAG :: CORRECT OR INCORRECT OR ANSWER (IF STMT)
            self.response.write("<br>")
            self.response.write(CLOSE_CSS_HTML)                                     #STYLESHEET CLASS - CLOSING TAG :: QUESTION
        self.response.write(CLOSE_CSS_HTML)                                         #STYLESHEET CLASS - CLOSING TAG :: QUESTION-BODY


        if is_add:                                                                  #STATIC LAB: SAVE DATA; GENERATE CORRECTED LAB 
            self.__add_responses__(user_object,lab_id,select,correct_answers)
                                                        
        if lab_id!=4444:
            self.response.write(FORM_HTML.substitute(action="/DynamicLab/"          #DYNAMIC LAB: AT BOTTOM OF CORRECTED LAB, CREATE FORM CONTAINING CHECKLIST OF TOPICS SUGGESTED FOR CUSTOM PROBLEM SET BASED ON USER WEAKNESSES
                                                     +str(lab_id)+"/",
                                                     method="link"))
            for i in range(len(topics)):
                isCheck=""
                if correct[i]*100.0/totals[i]<50:                                   #IF USER SCORES <50% IN A TOPIC, CUSTOM PROBLEMS ARE SUGGESTED FOR THAT TOPIC
                    isCheck="checked"
                self.response.write(CHECKBOX_HTML.substitute(name="topics",         #USER CAN OPT OUT OF TOPICS IN CUSTOM PROB SET BY UNCHECKING RESPECTIVE BOX
                                                             checked=isCheck,
                                                             value=topics[i],
                                                             text=topics[i]))
            self.response.write(SUBMIT_HTML.substitute(value="Get Practice Problems"))
            self.response.write(CLOSE_FORM_HTML)
        else:
            self.response.write(FORM_HTML.substitute(action="/",method="link"))
            self.response.write(SUBMIT_HTML.substitute(value="Return to main page"))
            self.response.write(CLOSE_FORM_HTML)
        self.response.write(CLOSE_HTML)

    def __check_login__(self):
        username = users.get_current_user()
        return userclass.sign_in(self,username.nickname())
        

