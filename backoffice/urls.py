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
    path('get_staff/', views.getStaff, name='get_staff'),

    path('profile/', views.profile, name='profile'),
    path('taxes/', views.taxes, name='taxes'),
    path('payroll/', views.payroll, name='payroll'),
    path('benefits/', views.benefits, name='benefits'),
    path('learning_management/', views.learning_management, name='learning_management'),
    path('team/', views.team, name='team'),
    path('new_email/<int:pk>', views.new_email, name='new_email'),
    path('select_email_template/', views.select_email_template, name='select_email_template'),
    path('new_course/', views.new_course, name='new_course'),

    path('staff/new/', views.new_staff, name='new_staff'),
    path('staff/<int:pk>/remove/', views.remove_staff, name='remove_staff'),
    path('staff/<int:pk>/edit/', views.edit_staff, name='edit_staff'),

    path('new_company/', views.new_company, name='new_company'),
    path('new_meeting/', views.new_meeting, name='new_meeting'),
    path('new_meeting/<int:pk>/', views.new_meeting, name='new_meeting'),

    path('new_test/<int:pk>/', views.new_test, name='new_test'),

    path('settings/', views.settings, name='settings'),
    path('quiz/', QuizListView.as_view(), name='quiz'),
    path('quiz/<int:pk>/', views.quiz_view, name='quiz-view'),
    path('quiz/<pk>/data/', views.quiz_data_view, name='quiz-data-view'),
    path('quiz/<pk>/save/', views.save_quiz_view, name='save-view'),
    path('quiz/<int:pk>/remove', views.remove_quiz, name='remove_quiz'),
    path('quiz/<int:pk>/edit', views.edit_quiz, name='edit_quiz'),



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
]
