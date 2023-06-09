from django import forms
from django.forms import ClearableFileInput
from .models import Staff, Course, Manager, Company, Country, Currency, Subscription, User, Job, Meeting, Quiz, EmailMessage
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.conf import settings


class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        help_text='Company Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': "eg. LLC MyCompany" }),
        required=True
        )
    mailing_address = forms.CharField(
        help_text='Mailing Address',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': "Chalk Butte Rd, Cut Bank, MT 59427"}),
        required=False
        )
    physical_address = forms.CharField(
        help_text='Physical Address',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': "Chalk Butte Rd, Cut Bank, MT 59427"}),
        required=False
    )
    taxpayerNumber = forms.CharField(
        help_text='Taxpayer Number',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': "eg. 7604272384" }),
        required=True
    )

    country = forms.ChoiceField(
        help_text='Company country',
        choices=Company.COUNTRIES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        required=True
    )
    currency = forms.ChoiceField(
        help_text='Company currency',
        choices=Company.CURRENCIES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        required=True
    )

    responsible_manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    subscription = forms.ModelChoiceField(
        queryset=Subscription.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    professional_area = forms.ChoiceField(
        help_text='Professional Area',
        choices=Company.PROFESSIONAL_AREAS,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        required=True
    )

    class Meta:
        model = Company
        fields = ['name', 'taxpayerNumber', 'country', 'mailing_address', 'physical_address', 'currency', 'professional_area']


class CourseForm(forms.ModelForm):
    title = forms.CharField(help_text='Course Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(
        help_text='Course Description',
        widget=forms.Textarea(attrs={'id': "body_editor", 'style': 'display:none;'}),
        required=False
    )

    job_title = forms.ModelMultipleChoiceField(
        queryset=Job.objects.all(),
        help_text='Applied for',
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': "choices-multiple-remove-button", 'name': "choices-multiple-remove-button"}),
        required=False
    )
    files = forms.FileField(
        help_text="Additional File",
        widget = forms.FileInput(
            attrs={'class': 'form-control dropzone',
                   'id': 'myDropzone'}),
        required=False
    )
    date_added = forms.DateField(
        help_text='Start Date',
        widget=forms.DateInput(format='%Y-%m-%d',
                               attrs={'class': 'form-control datetimepicker',
                                      'placeholder': "Start date"}),
        required=False
    )
    comment = forms.CharField(
        help_text='Comment',
        widget=forms.TextInput(attrs={'class': 'form-control mb-4'}),
        required = False
    )

    class Meta:
        model = Course
        fields = ['title', 'body', 'job_title', 'date_added', 'files', 'comment']


class JobForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(JobForm, self).__init__(*args, **kwargs)
        company = Company.objects.filter(responsible_manager__user=self.user).first()
        self.fields['responsible_manager'].widget = forms.Select(attrs={'class': 'form-select form-select-lg mb-3'})
        self.fields['responsible_manager'].queryset = company.responsible_manager.all()
        self.fields['responsible_manager'].help_text = 'Manager'

    title = forms.CharField(help_text='Job Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        help_text='Job Description',
    )

    #responsible_manager = forms.ModelChoiceField(
    #    queryset=Company.responsible_manager.filter(),
    #    help_text='Manager',
    #    widget=forms.Select(attrs={'class': 'form-control'}),
    #    required=True
    #)

    def save(self, *args, **kwargs):
        instance = super(JobForm, self).save(commit=False)
        instance.company = Company.objects.filter(responsible_manager__user=self.user).first()
        instance.save()
        return instance


    class Meta:
        model = Job
        fields = ['title', 'description', 'responsible_manager']


class StaffForm(forms.ModelForm):
    email = forms.EmailField(
        help_text='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Email'}))

    first_name = forms.CharField(
        help_text='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'First Name'}))

    last_name = forms.CharField(
        help_text='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Last Name'}))

    job = forms.ModelChoiceField(
        queryset=Job.objects.all(),
        help_text='Job Title',
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': "choices-multiple-remove-button",
                                           'name': "choices-multiple-remove-button"}),
        required=False
    )

    status = forms.ChoiceField(
        choices=Staff.type_status,
        help_text='Staff Status',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    username = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False
    )

    password = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Staff
        fields = ['email', 'first_name', 'last_name', 'job', 'status', 'cv']


class LoginForm(forms.Form):
    email = forms.EmailField(
        help_text='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Email'}))
    password = forms.CharField(
        help_text='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    username = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = User
        fields = ['email', 'password', "username"]


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        help_text='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Your Name'}),
        required=True
    )
    email = forms.CharField(
        help_text='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Email'}),
        required=True
    )
    password1 = forms.CharField(
        help_text='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )

    password2 = forms.CharField(
        help_text='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )

    username = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = User
        fields = ["first_name", "email", "password1", "password2", "username"]


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        help_text='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )
    new_password1 = forms.CharField(
        help_text='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )
    new_password2 = forms.CharField(
        help_text='New Password Repeat',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )


class ResetPasswordForm(PasswordResetForm):
    email = forms.CharField(
        help_text='Your Email',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Email'}),
        required=True
    )


class ActivatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        help_text='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )
    new_password2 = forms.CharField(
        help_text='New Password Repeat',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        required=True
    )


class ManagerForm(forms.ModelForm):

    first_name = forms.CharField(
        help_text='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'First Name'}))

    last_name = forms.CharField(
        help_text='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Last Name'}))

    phone = forms.CharField(
        max_length=100,
        help_text='Your phone',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': "eg. +1(444)2392-23-23"}),
        required=False
    )

    comment = forms.CharField(help_text='Комментарий', widget=forms.Textarea, required=False)


    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    #birthday = models.DateField(null=True, blank=True)


    class Meta:
        model = Manager
        fields = ["first_name", "last_name", "phone", "comment"]


class MeetingForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        print(user)
        super(MeetingForm, self).__init__(*args, **kwargs)
        company = Company.objects.filter(responsible_manager__user=self.user).first()
        self.fields['responsible_manager'].widget = forms.Select(attrs={'class': 'form-select form-select-lg mb-3'})
        self.fields['responsible_manager'].queryset = company.responsible_manager.all()
        self.fields['responsible_manager'].help_text = 'Manager'

    title = forms.CharField(help_text='Meeting Title', widget=forms.TextInput(attrs={'class': 'form-control'}))

    #responsible_manager = forms.ModelChoiceField(
    #    queryset=Manager.objects.all(),
    #    help_text='Responsible Manager',
    #    widget=forms.Select(attrs={'class': 'form-control', 'id': "choices-multiple-managers-button",
    #                                       'name': "choices-multiple-managers-button"}),
    #    required=False
    #)

    applicant = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        help_text='Applicants',
        widget=forms.Select(attrs={'class': 'form-control', 'id': "choices-multiple-applicants-button",
                                           'name': "choices-multiple-applicants-button"}),
        required=True
    )

    meeting_time = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control datetimepicker', 'display': 'none;',
                                      'placeholder': "Meeting datetime"}),
        required=False
    )

    questions = forms.ModelChoiceField(
        queryset=Quiz.objects.filter(status='interview'),
        help_text='Select Interview Question',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Meeting
        fields = ['title','company', 'responsible_manager', 'meeting_time', 'questions', 'applicant']



class EmailForm(forms.ModelForm):
    header = forms.CharField(help_text='Email Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(
        help_text='Email Body',
        widget=forms.Textarea(attrs={'id': "body_editor", 'style': 'display:none;'}),
        required=True
    )

    receivers = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.all(),
        help_text='Receivers',
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': "choices-multiple-applicants-button",
                                           'name': "choices-multiple-applicants-button"}),
        required=True
    )

    comment = forms.CharField(
        help_text='Comment',
        widget=forms.TextInput(attrs={'class': 'form-control mb-4'}),
        required = False
    )

    class Meta:
        model = EmailMessage
        fields = ['header', 'body', 'receivers', 'comment']


class QuizForm(forms.ModelForm):
    title = forms.CharField(help_text='Quiz Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        help_text='Description',
        widget=forms.TextInput(attrs={'class': 'form-control mb-4'}),
        required=False
    )

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'applied_for']