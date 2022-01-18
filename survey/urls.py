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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('', views.testing, name='testing'),
#    path('add_quiz/', views.add_quiz, name='add_quiz'),
#    path('add_question/', views.add_question, name='add_question'),
#    path('add_options/<int:myid>/', views.add_options, name='add_options'),
#    path('results/', views.results, name='results'),
#    path('delete_question/<int:myid>/', views.delete_question, name='delete_question'),
#    path('delete_result/<int:myid>/', views.delete_result, name='delete_result'),
]
