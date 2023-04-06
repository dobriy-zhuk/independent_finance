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
from .sitemaps import MainSitemap
from blog.sitemaps import BlogSitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'blog': BlogSitemap,
    'main_site': MainSitemap
}


urlpatterns = [
    path('', views.index, name='index'),
    path('price/', views.price, name='price'),
    path('teacher_hire/', views.teacher_hire, name='teacher_hire'),
    path('teacher_join/', views.teacher_join, name='teacher_join'),
    path('contacts/', views.contacts, name='contacts'),
    path('test_form/', views.test_form, name='test_form'),
    path('full_contact/', views.full_contact, name='full_contact'),
    path('payment/', views.payment, name='payment'),
    path('payment_paddle/', views.payment_paddle, name='payment_paddle'),

    path("robots.txt", views.robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
