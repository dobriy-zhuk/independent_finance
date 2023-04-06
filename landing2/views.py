# -*- encoding: utf-8 -*-

from django.shortcuts import render

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


def index(request):
    return render(request, 'landing2/index.html', {})


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        return render(request, f'landing2/{load_template}.html', {})

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('landing2/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('landing2/page-500.html')
        return HttpResponse(html_template.render(context, request))
