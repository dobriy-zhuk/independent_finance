from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Staff, Subscription, Manager, Course, Company, Meeting, Quiz, EmailTemplate, Job, ApplicantContent, InterviewSlot
from survey.models import Marks_Of_User
from .forms import CourseForm, CompanyForm, ManagerForm, LoginForm, RegisterForm, StaffForm, MeetingForm, QuizForm, ChangePasswordForm, ResetPasswordForm, EmailForm, JobForm, ActivatePasswordForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.core import serializers
import json
from django.views.generic import ListView
from django.http import JsonResponse
from survey.models import Question, Answer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Template, Context
from .tasks import send_email_with_delay
from django.forms.models import inlineformset_factory
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import gettext
from django.urls import reverse
from django.core.files.storage import FileSystemStorage


#Функция для отправки емайлов
def send_email_with_template(title, to, body):
    htmly = Template(body)

    content = {'name': "Artem",
               'position': "position",
               'time': "time"}

    html_content = htmly.render(Context(content))
    msg = EmailMultiAlternatives(title, html_content,
                                 "Гарантия Знаний <info@garantylearning.com>", to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

from django.template import loader
@login_required(login_url='signin')
def backoffice(request):

    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            #Create and save new company
            company = company_form.save(commit=False)
            company.subscription = Subscription.objects.all().first()
            company.save()
            company.responsible_manager.add(Manager.objects.get(user=request.user))

            #create email templates for new company
            interview_data = render_to_string("emails/interview.txt",
                                    {
                                        "manager": request.user.first_name,
                                    }
                                    )
            EmailTemplate(company=company, name="Interview",
                                            text=interview_data).save()

            meeting_data = render_to_string("emails/meeting.txt",
                                              {
                                                  "manager": request.user.first_name,
                                              }
                                              )
            EmailTemplate(company=company, name="Meeting",
                          text=meeting_data).save()

            offer_data = render_to_string("emails/offer.txt",
                                              {
                                                  "manager": request.user.first_name,
                                              }
                                              )
            EmailTemplate(company=company, name="Offer",
                          text=offer_data).save()

            return redirect('backoffice')
    else:
        company = Company.objects.filter(responsible_manager__user=request.user).first()
        company_form = CompanyForm(instance=company)

    applicants = Staff.objects.all().order_by('user')

    #{% url 'edit_company' pk=company.pk %}

    return render(request, 'backoffice/backoffice.html', {'applicants': applicants, 'company_form': company_form})


@login_required(login_url='signin')
def jobs(request):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        jobs = Job.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by('user')
    else:
        jobs = Job.objects.all()

    return render(request, 'backoffice/jobs.html', {'jobs': jobs,})


@login_required(login_url='signin')
def open_jobs(request):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        jobs = Job.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by('user')
    else:
        jobs = Job.objects.filter(status='open')
        print(jobs)

    return render(request, 'backoffice/open-jobs.html', {'jobs': jobs,})


@login_required(login_url='signin')
def template_jobs(request):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        jobs = Job.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by('user')
    else:
        jobs = Job.objects.filter(status='template')
        print(jobs)

    return render(request, 'backoffice/template-jobs.html', {'jobs': jobs,})


@login_required(login_url='signin')
def archive_jobs(request):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        jobs = Job.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by('user')
    else:
        jobs = Job.objects.filter(status='archive')

    return render(request, 'backoffice/open-jobs.html', {'jobs': jobs,})


@login_required(login_url='signin')
def show_staff(request, job_pk):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        applicants = Staff.objects.filter(Q(job=job_pk)&(Q(user__name__iexact=search_query) | Q(phone=search_query))).order_by('user')
    else:
        applicants = Staff.objects.filter(job=job_pk)

    return render(request, 'backoffice/applicants.html', {'applicants': applicants, 'job_pk': job_pk})


def getStaffList(View):
    page_limit = 10

    search_query = request.GET.get('q')

    # all_applicants = None
    if search_query:
        all_applicants = Staff.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by(
            'user')
    else:
        all_applicants = Staff.objects.all().order_by('user')

    def get_paginated_context(self, queryset, page, limit):
        if not page:    page = 1  # if no page provided, set 1

        # if limit specified, set the page limit
        if limit:
            self.page_limit = limit

            # instantiate the paginator object with queryset and page limit
        paginator = Paginator(queryset, self.page_limit)
        # get the page object
        page_obj = paginator.get_page(page)
        # serialize the objects to json
        serialized_page = serialize("json", page_obj.object_list)
        # get only required fields from the serialized_page json.
        serialized_page = [obj["fields"] for obj in json.loads(serialized_page)]

        # return the context.
        return {
            "data": serialized_page,
            "pagination": {
                "page": page,
                "limit": limit,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "total": queryset.count()
            }
        }

    def get(self, request, *args, **kwargs):
        # fetch the query params
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        name = request.GET.get('name')
        start = request.GET.get('start')
        end = request.GET.get('end')

        sort_by = request.GET.get('sort_by')
        # get all results from DB.
        queryset = Staff.objects.all()

        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if name and name != "all":
            queryset = queryset.filter(user__name=name)
        # 2. On basis of date (start and end date)
        if start and end:
            if start != "0" and end != "0":
                queryset = queryset.filter(
                    year__gte=start,
                    year__lte=end
                )

        # 3. Sorting the filtered queryset
        if sort_by and sort_by != "0":
            queryset = queryset.order_by(sort_by)

        # return the serialized output by
        # calling method 'get_paginated_context'
        to_return = self.get_paginated_context(queryset, page, limit)
        return JsonResponse(to_return, status=200)


def getStaff(request, pk):
    # get Staff from the database
    # excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        name = request.GET.get('name')

        sort_by = request.GET.get('sort_by')

        '''filter the queryset object based on query params'''
        if name:
            queryset = Staff.objects.values('user__first_name', 'user__last_name', 'job_title', 'user__email', 'phone',
                                            'status', 'id').filter(Q(job_title=pk)&(Q(user__first_name__contains=name) | Q(user__last_name__contains=name) | Q(phone=name)))
        else:
            queryset = Staff.objects.values('user__first_name', 'user__last_name', 'job_title__title', 'user__email', 'phone', 'status__title', 'id').filter(Q(job_title=pk))

        return JsonResponse(list(queryset), safe=False)


@login_required(login_url='signin')
def interview(request):
    meetings = Meeting.objects.all().order_by('meeting_time')[:5]

    context = {'meetings': meetings}

    return render(request, 'backoffice/interview.html', context)


@login_required(login_url='signin')
def new_email(request, template_name, applicant_pk):

    template_email = EmailTemplate.objects.filter(pk=applicant_pk).first()

    if request.method == "POST":
        email_form = EmailForm(request.POST)
        sending_time = request.POST["sending_time"]
        print(sending_time)
        if email_form.is_valid() and sending_time:
            email_form.save()
            to = []
            for applicant in email_form.cleaned_data['receivers']:
                to.append(applicant.user.email)

            send_email_with_delay.apply_async((email_form.cleaned_data['header'], to, email_form.cleaned_data['body']), eta=sending_time)
    else:
        email_form = EmailForm()
    return render(request, 'backoffice/new_email.html', {"email_form": email_form, 'template': template_email.text})


#Send email to applicant
@login_required(login_url='signin')
def send_email(request, template_name, applicant_pk):

    company = Company.objects.filter(responsible_manager__user=request.user).first()
    template_email = EmailTemplate.objects.filter(name=template_name, company=company).first()

    if request.method == "POST":
        email_form = EmailForm(request.POST)
        sending_time = request.POST["sending_time"]
        if email_form.is_valid():
            email_form.save()
            to = []
            for applicant in email_form.cleaned_data['receivers']:
                #to.append(applicant.user.email
                if sending_time:
                    send_email_with_delay.apply_async((email_form.cleaned_data['header'], [applicant.user.email], email_form.cleaned_data['body'], str(applicant.user.first_name), 'responsible_manager'), eta=sending_time)
                else:
                    send_email_with_delay(email_form.cleaned_data['header'], [applicant.user.email], email_form.cleaned_data['body'], str(applicant.user.first_name), 'responsible_manager')
    else:
        email_form = EmailForm()
        email_form.initial['header'] = template_email.title
        email_form.initial['receivers'] = get_object_or_404(Staff, pk=applicant_pk)

    return render(request, 'backoffice/send_email.html', {"email_form": email_form, 'template': template_email, 'applicant_pk': applicant_pk})


# TODO: set current user for form and check form! Set paid date etc!
def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        company_form = CompanyForm(request.POST, instance=company)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.subscription = Subscription.objects.all().first()
            company.responsible_manager = Manager.objects.all().first()
            company.save()
            return redirect('backoffice')
    else:
        company_form = CompanyForm(instance=company)

    return render(request, 'backoffice/edit_company.html', {"company_form": company_form})


def new_course(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
            return redirect('learning_management')
    else:
        course_form = CourseForm()

    return render(request, 'backoffice/new_course.html', {"course_form": course_form})


@login_required(login_url='signin')
def view_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    return render(request, "landing/course.html", {"course": course })


@login_required(login_url='signin')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course_form = CourseForm(request.POST, instance=course)

        if course_form.is_valid():
            course_form.save()

        return redirect("learning_management")

    else:
        course_form = CourseForm(instance=course)

    return render(request, "backoffice/edit_course.html", {"course_form": course_form })


@login_required
def remove_course(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        course.delete()
    except Course.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('backoffice')

    except Exception as e:
        return redirect('backoffice', {'err':e.message})

    return redirect('learning_management')


def new_job(request):
    if request.method == "POST":
        job_form = JobForm(request.user, request.POST)
        if job_form.is_valid():
            job_form.save()
            return redirect('show_jobs')
    else:
        company = Company.objects.filter(responsible_manager__user=request.user).first()
        manager = Manager.objects.get(user=request.user)
        job_form = JobForm(request.user)

    return render(request, 'backoffice/new_job.html', {"job_form": job_form})


def create_job_from_template(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        job_form = JobForm(request.user, request.POST, instance=job)
        if job_form.is_valid():
            job_form.save()
            return redirect('open_jobs')
    else:
        job_form = JobForm(request.user, instance=job)

    return render(request, 'backoffice/new_job.html', {"job_form": job_form})


@login_required(login_url='signin')
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == "POST":
        job_form = JobForm(request.POST, instance=job)

        if job_form.is_valid():
            job_form.save()

        return redirect("show_jobs")

    else:
        job_form = JobForm(instance=job)

    return render(request, "backoffice/edit_job.html", {"job_form": job_form })


@login_required
def remove_job(request, pk):
    try:
        job = get_object_or_404(Job, pk=pk)
        job.delete()
    except Job.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('backoffice')

    except Exception as e:
        return redirect('backoffice', {'err':e.message})

    return redirect('show_jobs')


@csrf_exempt
@require_POST
def new_staff_api(request):

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    token = request.POST.get('token')
    cv = request.FILES['cv_file']

    user, created = User.objects.get_or_create(username=email,
                                               email=email)
    user.first_name = name
    if created:
        user.set_password("GuaranteeHR!")
        user.save()
        user.refresh_from_db()

    job = get_object_or_404(Job, token=token)
    print(job)
    if Staff.objects.filter(user=user, job=job).first() is None:

        staff, created = Staff.objects.get_or_create(user=user, job=job)
        print(staff, created)
        staff.phone = phone
        staff.comment = token
        staff.save()

    return JsonResponse({'result': 'success'})


def new_staff(request):
    if request.method == "POST":
        staff_form = StaffForm(request.POST, request.FILES)
        if staff_form.is_valid():
            cd = staff_form.cleaned_data
            staff = staff_form.save(commit=False)
            user = User.objects.create_user(username=cd['email'],
                                            email=cd['email'],
                                            password="GuaranteeHR!",
                                            first_name=cd['first_name'],
                                            last_name=cd['last_name']
                                            )
            user.save()
            user.refresh_from_db()
            staff.user = User.objects.get(email=user.username)
            staff.save()
            staff_form.save_m2m()
            return redirect('backoffice')
    else:
        staff_form = StaffForm()
    return render(request, 'backoffice/new_staff.html', {"staff_form": staff_form})


@login_required
def remove_staff(request, pk):
    try:
        staff = get_object_or_404(Staff, pk=pk)
        staff.delete()
    except Staff.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('backoffice')

    except Exception as e:
        return redirect('backoffice', {'err':e.message})

    return redirect('backoffice')


@login_required(login_url='signin')
def edit_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)

    if request.method == "POST":
        staff_form = StaffForm(request.POST, instance=staff)
        if staff_form.is_valid():
            cd = staff_form.cleaned_data
            user = get_object_or_404(User, pk=staff.user.pk)
            user.email = cd["email"]
            user.first_name = cd["first_name"]
            user.last_name = cd["last_name"]
            user.save()
            staff_form.save()

        return redirect("backoffice")
    else:
        staff_form = StaffForm(instance=staff)
        staff = get_object_or_404(Staff, pk=pk)
        staff_form.initial['email'] = staff.user.email
        staff_form.initial['first_name'] = staff.user.first_name
        staff_form.initial['last_name'] = staff.user.last_name

    return render(request, "backoffice/edit_staff.html", {"staff_form": staff_form })


def view_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'backoffice/job_description.html', {'job': job})


def meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    applicant_test = Marks_Of_User.objects.filter(user=meeting.applicant.user)
    return render(request, 'backoffice/meeting.html', {'meeting': meeting, 'applicant_test': applicant_test})


def meeting_test(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    applicant_test = Marks_Of_User.objects.filter(user=meeting.applicant.user)
    return render(request, 'landing/interview.html', {'meeting': meeting, 'applicant_test': applicant_test})


def time_interview(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    slot = request.GET.get('slot', None)
    if slot is not None and slot != '':
        meeting.meeting_time = datetime.datetime.fromisoformat(slot[:-1] + '+00:00').astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        meeting.save()
        messages.success(request, "SUCCESS!")


    #applicant_test = Marks_Of_User.objects.filter(user=meeting.applicant.user)
    return render(request, 'landing/interview_time_selector.html', {'meeting': meeting})


def save_slot(request):
    responsible_manager = Manager.objects.get(user=request.user)

    day, time =request.POST['slot'].split('_')
    status = True if request.POST.get("status") == "true" else False
    interview_slot, created = InterviewSlot.objects.get_or_create(responsible_manager=responsible_manager,
                                                         day=day,
                                                         time=time)
    interview_slot.is_active = status
    interview_slot.save()

    if request.method == 'POST':
        return JsonResponse({'result': 'ok'}, safe=False)


#Обработка слотов и вывод доступных за исключением забронированных на meeting
def get_interview_slots(request, responsible_manager_id):

    try:
        responsible_manager = User.objects.get(id=responsible_manager_id)

        result = []

        for i in range(1, 14):
            date = datetime.datetime.today().date() + datetime.timedelta(days=i)
            day = date.weekday() + 1

            #Все свободные слоты менеджера
            time_slots = InterviewSlot.objects.filter(responsible_manager__user=responsible_manager, day=day,
                                                      is_active=True).values('time').order_by('time')

            slots = []
            #Проходим по каждому елементу из слота менеджера и сравнивам с его временем встреч
            for elem in time_slots:
                elem_time = datetime.datetime.combine(date, timezone.make_aware(elem["time"], timezone.utc))

                if not Meeting.objects.filter(responsible_manager__user=responsible_manager,
                                              meeting_time=elem_time).exists():
                    slots.append(elem_time)

            result.append({'date': date, 'day': day, 'slots': slots})

        return JsonResponse({"slots": result}, safe=False)

    except User.DoesNotExist:
        print("Manager is not exist")
        return JsonResponse({'result': 'Error: manager is not exist'}, safe=False)


def get_manager_slots(request, responsible_manager_id):
    try:
        responsible_manager = User.objects.get(id=responsible_manager_id)
        time_slots = InterviewSlot.objects.filter(responsible_manager__user=responsible_manager).values('day', 'time',
                                                                                                        'is_active').order_by('day', 'time')
        for t in time_slots:
            t["time"] = t["time"].strftime("%I:%M %p")
            t["end_time"] = datetime.datetime.strptime(t["time"], "%I:%M %p") + datetime.timedelta(hours=1)
            t["end_time"] = t["end_time"].strftime("%I:%M %p")

        return JsonResponse({"slots": list(time_slots)}, safe=False)

    except User.DoesNotExist:
        print("Manager is not exist")
        return JsonResponse({'result': 'Error: manager is not exist'}, safe=False)

"""

{
date + time: 21 nov 2022 8 am
link


"""


def view_staff(request, pk):
    applicant = get_object_or_404(Staff, pk=pk)
    tests = Marks_Of_User.objects.filter(user__pk=pk)
    return render(request, 'backoffice/applicant.html', {'applicant': applicant, 'tests': tests})


def profile(request):
    return render(request, 'backoffice/profile.html', {})


def test_library(request):
    quizes = Quiz.objects.all()
    context = {'quizes': quizes}
    return render(request, 'backoffice/test_library.html', context)


def get_tests(request):
    if request.method == "GET" and request.is_ajax():
        status = request.GET.get('status')

        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if status:
            queryset = Quiz.objects.values('title', 'description', 'id').filter(Q(status=status))
            print(queryset)

            return JsonResponse(list(queryset), safe=False)


def save_content(request):
    applicant_content = get_object_or_404(ApplicantContent, info=0)
    applicant_content.text = request.GET.get('content')
    applicant_content.save()
    return HttpResponse("so")


def get_content(request):
    if request.method == "GET" and request.is_ajax():
        status = request.GET.get('status')

        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if status:
            queryset = Quiz.objects.values('title', 'description', 'id').filter(Q(status=status))
            print(queryset)

            return JsonResponse(list(queryset), safe=False)


def payroll(request):
    return render(request, 'backoffice/profile.html', {})


def team(request):
    company = Company.objects.filter(responsible_manager__user__exact=request.user).first()
    team = company.responsible_manager.all()

    return render(request, 'backoffice/team.html', {'team': team})


def learning_management(request):
    all_courses = Course.objects.all()
    return render(request, 'backoffice/lerarning_managment.html', {'courses': all_courses})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('backoffice')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Check you login and password')
                return redirect('signin')
    else:
        form = LoginForm()
    return render(request, 'backoffice/sign_in.html', {'form': form})



@login_required
def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.username = cd['email']
            user.first_name = cd['first_name']
            user.save()
            user.refresh_from_db()

            Manager.objects.get_or_create(user=user)
            if Manager.objects.get(user=user) is None:
                return HttpResponse('We couldn`t find your account')
            else:
                if user.is_active:
                    login(request, user)
                    return redirect('backoffice')
                else:
                    return HttpResponse('Disabled account')
            #manager.save()
            #staff_form.save_m2m()
            #return redirect('backoffice')

        #if form.is_valid():
       #     user = authenticate(username=cd['email'], password=cd['password2'])
        #    if user is not None:
         #       if user.is_active:
         #           login(request, user)
         #           return redirect('backoffice')
         #       else:
         #           return HttpResponse('Disabled account')
    else:
        form = RegisterForm()

    return render(request, 'backoffice/sign_up.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was updated!')
            return redirect('backoffice')
        else:
            messages.error(request, 'Update error. Try again')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'backoffice/change_password.html', {
        'form': form
    })


def reset_password(request):

    if request.method == "POST":
        password_reset_form = ResetPasswordForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "GuaranteeHR: password recovery information"
                    email_template_name = "emails/password_reset.txt"
                    c = {
                        "email": user,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'GuaranteeHR',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'info@garantylearning.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'Password recovery information has been sent to your email')
                    return redirect("signin")
    password_reset_form = ResetPasswordForm()
    return render(request, 'backoffice/reset_password.html', context={"form": password_reset_form})


def password_reset_complete(request):
    messages.success(request, 'The data is saved!')
    return redirect('signin')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ActivatePasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important! ???
                user.is_active = True
                user.save()

                manager, created = Manager.objects.get_or_create(user=user)
                if created:
                    for day_number in range(1,7):
                        for day_time in (datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0)) + datetime.timedelta(hours=n) for n in range(12)):
                            interview_slot, created = InterviewSlot.objects.get_or_create(
                                responsible_manager=manager,
                                day=day_number,
                                time=day_time)
                            interview_slot.is_active = True
                            interview_slot.save()

                company = Company.objects.create(email=manager.user.email)
                company.responsible_manager.add(manager)
                company.save()

                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Your password was saved!')
                    return redirect('backoffice')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Update error. Try again')
        else:
            form = ActivatePasswordForm(user)

        return render(request, 'backoffice/set_password.html', {
            'form': form
        })


        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def new_meeting(request, pk):
    if request.method == "POST":
        meeting_form = MeetingForm(request.user, request.POST)
        if meeting_form.is_valid():
            meeting_form.save()
    else:
        meeting_form = MeetingForm(request.user)
        try:
            meeting_form.initial['responsible_manager'] = Manager.objects.get(user=request.user)
            meeting_form.initial['applicant'] = get_object_or_404(Staff, pk=pk)
        except Staff.DoesNotExist:
            # messages.error(request, "User doesnot exist")
            # return render(request, 'front.html')
            print("Error find PK of applicant")

    return render(request, 'backoffice/new_meeting.html', {"meeting_form": meeting_form})



@login_required
def new_test(request, pk):
    if request.method == "POST":
        new_test_form = QuizForm(request.POST)
        if new_test_form.is_valid():
            new_test_form.save()
    else:
        new_test_form = QuizForm()
        try:
            new_test_form.initial['applicants'] = get_object_or_404(Staff, pk=pk)
        except Staff.DoesNotExist:
            # messages.error(request, "User doesnot exist")
            # return render(request, 'front.html')
            print("Error find PK of applicant")

    return render(request, 'backoffice/applicant_test.html', {"new_test_form": new_test_form})


@login_required
def new_quiz(request): #ADD ANSWER FORMSET
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()
            for form in question_formset.forms:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()

                for answer_form in form.nested.forms:
                    answer = answer_form.save(commit=False)
                    answer.question = question
                    answer.save()

            return redirect('test_library')
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet()

    return render(request, 'backoffice/applicant_test.html', {"quiz_form": quiz_form, 'question_formset': question_formset })


from survey.forms import QuestionFormSet, AnswerFormSet
@login_required(login_url='signin')
def edit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == "POST":
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = QuestionFormSet(request.POST, instance=quiz)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()
            for form in question_formset.forms:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()

                for answer_form in form.nested.forms:
                    answer = answer_form.save(commit=False)
                    answer.question = question
                    answer.save()

            return redirect('test_library')
    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(instance=quiz)


    return render(request, "backoffice/edit_quiz.html", {"quiz_form": quiz_form, 'question_formset': question_formset })


@login_required
def remove_quiz(request, pk):
    try:
        quiz = get_object_or_404(Quiz, pk=pk)
        quiz.delete()
    except Quiz.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('backoffice')

    except Exception as e:
        return redirect('backoffice', {'err':e.message})

    return redirect('test_library')


def testing(request):
    quizes = Quiz.objects.all()
    return render(request, 'backoffice/testing.html', {'quizes': quizes})


def price(request):
    return render(request, 'backoffice/pricing.html', {})


def settings(request):

    company = Company.objects.filter(responsible_manager__user=request.user).first()
    manager = Manager.objects.get(user=request.user)

    if request.method == "POST":
        company_form = CompanyForm(request.POST, instance=company)
        manager_form = ManagerForm(request.POST, instance=manager)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.subscription = Subscription.objects.all().first()
            company.save()
            return redirect('settings')

        if manager_form.is_valid():
            manager_form.save()
            return redirect('settings')
    else:
        company_form = CompanyForm(instance=company)
        manager_form = ManagerForm(instance=manager)

    context = {
        'company_form': company_form,
        'manager_form': manager_form
    }

    return render(request, 'backoffice/settings.html', context)


class QuizListView(ListView):
    model = Quiz
    template_name = 'backoffice/new_quiz.html'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'backoffice/quiz.html', {'obj': quiz})


def show_quiz(request, user_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    z = urlsafe_base64_encode(force_bytes(189))
    x = urlsafe_base64_decode(z)

    return render(request, 'backoffice/quiz.html', {'obj': quiz})

def applicant_quiz(request, user_pk, quiz_pk):
    #quiz = Quiz.objects.get(pk=quiz_pk)
    z = urlsafe_base64_encode(force_bytes(189))
    x = urlsafe_base64_decode(z)

    return render(request, 'landing/quiz.html', {})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []

    print(quiz.get_questions())
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({'question': str(q), 'answers': answers, 'type': str(q.type)})

    print({
        'data': questions
    })

    return JsonResponse({
        'data': questions
    })



def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        print("ook")

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score_)

        return JsonResponse({'passed': True, 'score': score_, 'results': results})



@login_required(login_url='signin')
def select_email_template(request, applicant_pk):
    company = Company.objects.filter(responsible_manager__user=request.user).first()
    email_templates = EmailTemplate.objects.filter(company=company)
    return render(request, 'backoffice/select_email_template.html', {
        'email_templates': email_templates,
        'applicant_pk': applicant_pk
    }
                  )
