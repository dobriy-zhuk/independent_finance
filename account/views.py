# -*- encoding: utf-8 -*-

from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url="signin")
def index(request):
    return render(request, 'account/index.html', {})



