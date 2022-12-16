from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import random
import uuid


from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets


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


class ApplicantContent(models.Model):
    info = models.IntegerField(blank=True)
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'ApplicantContents'

    def __str__(self):
        return self.text


class Subscription(models.Model):
    title = models.CharField(max_length=50, default="Standard")
    price = models.IntegerField(default=25)
    candidates = models.IntegerField(default=100)
    additional_candidate_price = models.FloatField(default=1.2)
    tests = models.IntegerField(default=5)
    valid_until = models.DateField(default=now, blank=True)
    ats_integration = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Subscriptions'

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
    name = models.CharField(max_length=300, default='My Company')
    description = models.CharField(max_length=300, blank=True)
    taxpayerNumber = models.CharField(max_length=300, unique=True)

    COUNTRIES = (
        ('UK', 'UK'),
        ('USA', 'USA'),
        ('Canada', 'Canada'),
    )
    country = models.CharField(
        max_length=20,
        choices=COUNTRIES,
        blank=True,
        default='USA',
        help_text='Countries',
    )

    mailing_address = models.TextField(blank=True)
    physical_address = models.TextField(blank=True)
    CURRENCIES = (
        ('USD', 'USD'),
        ('EURO', 'EURO'),
        ('POUND', 'POUND'),
    )
    currency = models.CharField(
        max_length=20,
        choices=CURRENCIES,
        blank=True,
        default='USD',
        help_text='Currencies',
    )
    subscription = models.ForeignKey(Subscription, default=1, on_delete=models.CASCADE)
    responsible_manager = models.ManyToManyField(Manager)
    date_added = models.DateField(default=now, blank=True)
    comment = models.TextField(blank=True)

    PROFESSIONAL_AREAS = (
        ('it', 'IT'),
        ('education', 'Education'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
    )
    professional_area = models.CharField(
        max_length=20,
        choices=PROFESSIONAL_AREAS,
        blank=True,
        default='it',
        help_text='Professional Areas',
    )

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name + "({0})".format(self.responsible_manager.all())


class Job(models.Model):
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=100, default="Seller")
    description = models.CharField(max_length=500, default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    responsible_manager = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True)
    status_list = (
        ("open", "open"),
        ("archive", "archive"),
        ("template", "template"),
    )
    status = models.CharField(max_length=50, choices=status_list, default="template")
    date_added = models.DateField(default=now, blank=True)
    address = models.CharField(max_length=500, default="", blank=True)

    class Meta:
        verbose_name_plural = 'jobs'

    def __str__(self):
        return self.title


class StaffSource(models.Model):
    title = models.CharField(max_length=30, default="Indeed")



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


#learning system for staff and new staff
class Course(models.Model):
    title = models.CharField(max_length=250, default="Training")
    body = models.TextField(default="")
    job_title = models.ManyToManyField(Job, blank=True)
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
    #number_of_questions = models.IntegerField(default=1)
    #required_score_to_pass = models.IntegerField(help_text="required score in %")
    status_list = (
        ("test", "test"),
        ("simulator", "simulator"),
        ("interview", "interview"),
    )
    status = models.CharField(max_length=50, choices=status_list, default="test")

    class Meta:
        verbose_name_plural = 'Quizes'

    def __str__(self):
        return f"{self.title}-{self.description}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:len(questions)]


class CompletedCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField()

    def __str__(self):
        return f"user: {self.user}, course: {self.course} - {self.completed}"


class Staff(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    salary = models.IntegerField(default=0, blank=True)
    currency = models.CharField(max_length=4, default="EUR", blank=True)
    phone = models.CharField(max_length=100, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    type_status = (
        ("Active", "Active"),
        ("Archive", "Archive"),
        ("Interview", "Interview"),
        ("Learning", "Learning"),
        ("Work", "Work"),
    )
    status = models.CharField(max_length=50, choices=type_status, default='Active')
    source = models.ForeignKey(StaffSource, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(blank=True)
    completed_courses = models.ManyToManyField(CompletedCourses, blank=True)
    cv = models.FileField(upload_to='documents/', default='blog/logo-rus.png')
    cv_uploaded_at = models.DateTimeField(auto_now_add=True)
    #script of dialog with clients
    #причина отказа
    #promotion = ForeignKey


    class Meta:
        verbose_name_plural = 'staff'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class Meeting(models.Model):
    title = models.CharField(max_length=300, default="Interview")
    company = models.ForeignKey(Company,on_delete=models.CASCADE, blank=True)
    responsible_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True)
    meeting_time = models.DateTimeField(default=now, blank=True)
    link = models.CharField(max_length=300, default=secrets.token_hex(5))
    questions = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class InterviewSlot(models.Model):
    responsible_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(default=1, blank=True)
    time = models.TimeField(max_length=300, default="08:00 AM", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{0}: {1} - {2} ({3})".format(self.responsible_manager, self.day, self.time, self.is_active)

    class Meta:
        unique_together = ('responsible_manager', 'day', 'time')


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


class EmailTemplate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, default="")
    title = models.TextField(default="", max_length=100, blank=True)
    text = models.TextField(default="", blank=True)
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

