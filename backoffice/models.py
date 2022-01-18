from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import random


from django.db.models.signals import post_save
from django.dispatch import receiver


class Country(models.Model):
    title = models.CharField(max_length=50, default="USA")

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.title


class Currency(models.Model):
    title = models.CharField(max_length=50, default="USD")

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    title = models.CharField(max_length=50, default="Standard")

    class Meta:
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return self.title


class StaffStatus(models.Model):
    title = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title


class StaffSource(models.Model):
    title = models.CharField(max_length=30, default="Indeed")

    class Meta:
        verbose_name_plural = 'staff_source'

    def __str__(self):
        return self.title


class JobTitle(models.Model):
    title = models.CharField(max_length=100, default="Seller")

    class Meta:
        verbose_name_plural = 'job_title'

    def __str__(self):
        return self.title


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    bank_details = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'managers'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class Company(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    mailing_address = models.TextField(blank=True)
    physical_address = models.TextField(blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    responsible_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    date_added = models.DateField(default=now, blank=True)
    subscription_until = models.DateField(default=now, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    salary = models.IntegerField(default=0, blank=True)
    currency = models.CharField(max_length=4, default="EUR", blank=True)
    phone = models.CharField(max_length=100, blank=True)
    bonus = models.PositiveIntegerField(default=0, blank=True)
    job_title = models.ManyToManyField(JobTitle, blank=True)
    status = models.ForeignKey(StaffStatus, on_delete=models.CASCADE, blank=True, null=True)
    source = models.ForeignKey(StaffSource, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(blank=True)
    #script of dialog with clients
    #причина отказа
    #promotion = ForeignKey


    class Meta:
        verbose_name_plural = 'staff'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class Settings(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    birthday = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=200, blank=True)
    currency = models.CharField(max_length=4, default="RUB")
    phone = models.CharField(max_length=100, blank=True)
    tariff = models.PositiveIntegerField(default=0)
    responsible_manager = models.ForeignKey(Manager, default=0, on_delete=models.CASCADE)
    date_added = models.DateField(default=now, blank=True)

    comment = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = 'settings'

    #def __str__(self):
    #    return "{0} {1}".format(self.user.first_name, self.user.last_name)


class EmailMessage(models.Model):
    header = models.CharField(max_length=300, default="")
    body = models.TextField(default="")
    receivers = models.ManyToManyField(Staff, blank=True)
    language = models.CharField(max_length=200, blank=True)
    date_added = models.DateField(default=now, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'EmailMessages'

#    def __str__(self):
#        return "{0} {1}".format(self.user.first_name, self.user.last_name)


#learning system for staff and new staff
class Course(models.Model):
    title = models.CharField(max_length=250, default="Training")
    body = models.TextField(default="")
    job_title = models.ManyToManyField(JobTitle, blank=True)
    files = models.FileField(upload_to='courses_files/', blank=True, null=True)
    date_added = models.DateField(default=now, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type_staff = (
        ("HR", "HR"),
        ("STAFF", "STAFF"),
        ("APPLICANT", "APPLICANT"),
    )
    applied_for = models.CharField(max_length=50, choices=type_staff)
    number_of_questions = models.IntegerField(default=1)
    #required_score_to_pass = models.IntegerField(help_text="required score in %")

    class Meta:
        verbose_name_plural = 'Quizes'

    def __str__(self):
        return f"{self.title}-{self.description}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]


class Meeting(models.Model):
    title = models.CharField(max_length=300, default="Interview")
    company = models.ForeignKey(Company,on_delete=models.CASCADE, blank=True, null=True)
    responsible_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(Staff)
    meeting_time = models.DateTimeField(default=now)
    link = models.CharField(max_length=300, default="mit.jit.si", blank=True)
    questions = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title



class EmailTemplate(models.Model):
    name = models.CharField(max_length=300, default="")
    template = models.TextField(default="", blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'EmailTemplates'

    def __str__(self):
        return self.name



#Compare with leader staff = Automatically

#free corporate courses for staff v2.0

#Screening of staff v2.0

#Blog - how to create HR - brand v2.0

#Time Tracking v2.0

