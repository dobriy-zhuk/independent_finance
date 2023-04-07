# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm


def signup(request):
    msg = None
    success = False

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #TODO: надо навесить триггер в БД, так как username=email обязательное условие для любых обновлений в БД.
            user.username = form.cleaned_data.get("email")
            user.save()

            username = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/account/login">login</a>.'
            success = True
        else:
            msg = 'Form is not valid'
    else:
        form = RegisterForm()

    return render(request, 'account/auth/register.html', {"form": form, "msg": msg, "success": success})


def signin(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd.get('email'), password=cd.get('password'))
            if user is not None:
                login(request, user)
                request.POST.get('next')
                return redirect(request.POST.get('next') or 'account')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, 'account/auth/login.html', {'form': form, "msg": msg})


def signout(request):
    logout(request)
    return redirect('signin')
