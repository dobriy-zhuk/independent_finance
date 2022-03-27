"""hr_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import QuizListView

urlpatterns = [
    path('', views.backoffice, name='backoffice'),
    path('get_staffList/', views.getStaffList, name='get_staff_list'),
    path('get_staff/<int:pk>/', views.getStaff, name='get_staff'),

    path('profile/', views.profile, name='profile'),
    path('test_library/', views.test_library, name='test_library'),
    path('payroll/', views.payroll, name='payroll'),
    path('team/', views.team, name='team'),
    path('learning_management/', views.learning_management, name='learning_management'),
    path('course/<int:pk>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:pk>/remove/', views.remove_course, name='remove_course'),
    path('interview/', views.interview, name='interview'),
    path('new_email/<int:applicant_pk>/', views.new_email, name='new_email'), #редактирование емайл шаблона
    path('send_email/<str:template_name>/<int:applicant_pk>', views.send_email, name='send_email'),#Отправка всех видов емайлов соискателям
    path('select_email_template/', views.select_email_template, name='select_email_template'),
    path('new_course/', views.new_course, name='new_course'),


    path('jobs/', views.jobs, name='show_jobs'),
    path('jobs/<int:pk>/edit', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/remove', views.remove_job, name='remove_job'),
    path('jobs/<int:pk>/view/', views.view_job, name='view_job'),
    path('staff/<int:job_pk>/', views.show_staff, name='show_staff'),
    path('staff/new/', views.new_staff, name='new_staff'),
    path('staff/<int:pk>/remove/', views.remove_staff, name='remove_staff'),
    path('staff/<int:pk>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:pk>/view/', views.view_staff, name='view_staff'),

    path('edit_company/<int:pk>/', views.edit_company, name='edit_company'),
    path('new_job/', views.new_job, name='new_job'),
    path('new_meeting/', views.new_meeting, name='new_meeting'),
    path('meeting/<int:pk>/', views.meeting, name='meeting'),
    path('new_meeting/<int:pk>/', views.new_meeting, name='new_meeting'),

    path('new_test/<int:pk>/', views.new_test, name='new_test'),

    path('settings/', views.settings, name='settings'),
    path('quiz/', QuizListView.as_view(), name='quiz'),
    path('quiz/<int:user_pk>/<int:quiz_pk>/', views.show_quiz, name='show_quiz'), #transfer to applicant system!
    path('quiz/<int:pk>/', views.quiz_view, name='quiz-view'),
    path('quiz/<pk>/data/', views.quiz_data_view, name='quiz-data-view'),
    path('quiz/<pk>/save/', views.save_quiz_view, name='save-view'),
    path('quiz/<int:pk>/remove', views.remove_quiz, name='remove_quiz'),
    path('quiz/<int:pk>/edit', views.edit_quiz, name='edit_quiz'),
    path('new_quiz/', views.new_quiz, name='new_quiz'),


    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="backoffice/reset_password_confirm.html"),
         name='reset_password_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),

    path('price/', views.price, name='price'),

    path('api/get_tests', views.get_tests, name='api_get_tests'),
    path('api/save_content', views.save_content, name='api_save_content'),
    path('api/get_content', views.get_content, name='api_get_content'),
    path('api/new_staff', views.new_staff_api, name='api_new_staff'),


    path('save_slot/', views.save_slot, name='save_slot'), #save slots for manager in settings page. TODO: Change to ONE JSON!
    path('get_interview_slots/<int:responsible_manager_id>/', views.get_interview_slots, name='get_interview_slots'), #get slots by job
    path('get_manager_slots/<int:responsible_manager_id>/', views.get_manager_slots, name='get_manager_slots'), #get slots by job


    #FOR APPLICANT
    path('quiz/<int:user_pk>/applicant/<int:quiz_pk>/', views.applicant_quiz, name='quiz_applicant'),
    path('meeting_test/<int:pk>/', views.meeting_test, name='meeting_test'),
    path('course/<int:pk>/view/', views.view_course, name='view_course'),
    path('time_interview/<int:pk>/', views.time_interview, name='time_interview'),
]
