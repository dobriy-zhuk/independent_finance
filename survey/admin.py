from django.contrib import admin
from .models import Question, Answer, Marks_Of_User


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Marks_Of_User)
