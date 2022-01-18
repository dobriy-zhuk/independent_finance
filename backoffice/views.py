from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Staff, Subscription, Manager, Course, Company, Meeting, Quiz, EmailTemplate
from .forms import CourseForm, CompanyForm, ManagerForm, LoginForm, RegisterForm, StaffForm, MeetingForm, QuizForm, ChangePasswordForm, ResetPasswordForm, EmailForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
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


@login_required(login_url='signin')
def backoffice(request):

    page_limit = 10
    search_query = request.GET.get('q')

    #all_applicants = None
    if search_query:
        all_applicants = Staff.objects.filter(Q(user__name__iexact=search_query) | Q(phone=search_query)).order_by('user')
    else:
        all_applicants = Staff.objects.all().order_by('user')



    return render(request, 'backoffice/hire.html', {'applicants': all_applicants,})


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


def getStaff(request):
    # get Staff from the database
    # excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        name = request.GET.get('name')

        sort_by = request.GET.get('sort_by')

        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if name:
            queryset = Staff.objects.values('user__first_name', 'user__last_name', 'job_title', 'user__email', 'phone',
                                            'status', 'id').filter(Q(user__first_name__contains=name) | Q(user__last_name__contains=name) | Q(phone=name))
        else:
            queryset = Staff.objects.values('user__first_name', 'user__last_name', 'job_title__title', 'user__email', 'phone', 'status__title', 'id')

        return JsonResponse(list(queryset), safe=False)

@login_required(login_url='signin')
def team(request):
    return render(request, 'backoffice/team.html', {})


@login_required(login_url='signin')
def new_email(request, pk):

    template_email = EmailTemplate.objects.filter(pk=pk).first()

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

    return render(request, 'backoffice/new_email.html', {"email_form": email_form, 'template': template_email.template})


# TODO: set current user for form and check form! Set paid date etc!
def new_company(request):
    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.subscription = Subscription.objects.all().first()
            company.responsible_manager = Manager.objects.all().first()
            company.save()
    else:
        company_form = CompanyForm()
    return render(request, 'backoffice/new_company.html', {"company_form": company_form})


def new_course(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
    else:
        course_form = CourseForm()

    return render(request, 'backoffice/new_course.html', {"course_form": course_form})


def new_staff(request):
    if request.method == "POST":
        staff_form = StaffForm(request.POST)
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


def profile(request):
    return render(request, 'backoffice/profile.html', {})


def taxes(request):
    return render(request, 'backoffice/billing.html', {})


def payroll(request):
    return render(request, 'backoffice/profile.html', {})


def benefits(request):
    return render(request, 'backoffice/rtl.html', {})


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


@login_required
def new_meeting(request, pk):
    if request.method == "POST":
        meeting_form = MeetingForm(request.POST)
        if meeting_form.is_valid():
            meeting_form.save()
    else:
        meeting_form = MeetingForm()
        try:
            meeting_form.initial['applicants'] = get_object_or_404(Staff, pk=pk)
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

from survey.forms import QuestionFormSet

@login_required(login_url='signin')
def edit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == "POST":
        quiz_form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormSet(request.POST, instance=quiz)


        if quiz_form.is_valid() and formset.is_valid():
            cd = quiz_form.cleaned_data
            quiz_form.save()
            formset.save()

        return redirect("settings")

    else:
        quiz_form = QuizForm(instance=quiz)
        formset = QuestionFormSet(instance=quiz)

    return render(request, "backoffice/edit_quiz.html", {"quiz_form": quiz_form, 'question_form': formset })


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

    return redirect('settings')


def testing(request):
    quizes = Quiz.objects.all()
    return render(request, 'backoffice/testing.html', {'quizes': quizes})


def price(request):
    return render(request, 'backoffice/pricing.html', {})


def settings(request):
    quizes = Quiz.objects.all()
    context = {'quizes': quizes}
    return render(request, 'backoffice/settings.html', context)



class QuizListView(ListView):
    model = Quiz
    template_name = 'backoffice/new_quiz.html'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'backoffice/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions
    })


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

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
        #Result.objects.create(quiz=quiz, user=user, score=score_) SAVE RESULT FOR USER

        return JsonResponse({'passed': True, 'score': score_, 'results': results})



@login_required(login_url='signin')
def select_email_template(request):
    email_templates = EmailTemplate.objects.all()
    return render(request, 'backoffice/select_email_template.html', {'email_templates': email_templates})