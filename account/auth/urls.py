# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin, name="login"),
    path('signin/', views.signin, name="signin"),
    path('register/', views.signup, name="register"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.signout, name="logout"),
    path('signout/', views.signout, name="signout"),
    path('auth/', views.signout, name="auth"),
]
