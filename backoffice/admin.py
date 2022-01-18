from django.contrib import admin
from .models import Staff, Manager, StaffSource, StaffStatus, JobTitle, Course, Company, Country, Currency, Subscription, Meeting, Quiz, EmailMessage, EmailTemplate
#from survey.models import SurveyStaff, Test, InterviewQuestions


admin.site.register(Company)
admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(StaffSource)
admin.site.register(StaffStatus)
admin.site.register(JobTitle)
admin.site.register(Course)
#admin.site.register(SurveyStaff)
#admin.site.register(Test)
admin.site.register(Currency)
admin.site.register(Subscription)
admin.site.register(Country)
admin.site.register(Quiz)
admin.site.register(Meeting)
admin.site.register(EmailMessage)
admin.site.register(EmailTemplate)
