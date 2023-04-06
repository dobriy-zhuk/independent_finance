# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from . import views


urlpatterns = [

    # The home page
    path('', views.index, name='landing2'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
