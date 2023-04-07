# -*- encoding: utf-8 -*-

from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='account'),
    path('', include("account.auth.urls")),
]
