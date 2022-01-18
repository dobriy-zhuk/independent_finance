from django.db import models
from django.contrib.auth.models import User
from backoffice.models import Quiz

import random

"""
class Test(models.Model):
    title = models.CharField(max_length=100, default="Seller")
    body = models.TextField(default="")
    #responsible_manager = models.ForeignKey(Manager, default=0, on_delete=models.CASCADE)
    answers = models.TextField(default="")
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title


class SurveyStaff(models.Model):
    title = models.CharField(max_length=100, default="Seller")
    body = models.TextField(default="")
    #responsible_manager = models.ForeignKey(Manager, default=0, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Survives'

    def __str__(self):
        return self.title


class InterviewQuestions(models.Model):
    title = models.CharField(max_length=500, default="Questions for IT manager")
    body = models.TextField(default="", blank=True)

    class Meta:
        verbose_name_plural = 'Interviews'

    def __str__(self):
        return self.title
"""


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)

