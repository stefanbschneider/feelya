from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Label


def index(request):
    labels = Label.objects.order_by('-date')
    template = loader.get_template('app/index.html')
    # output = ', '.join([l.name for l in labels])
    context = {
        'labels': labels,
    }
    return HttpResponse(template.render(context, request))
