from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Label


def index(request):
    labels = Label.objects.order_by('-date')
    template = loader.get_template('app/index.html')
    # output = ', '.join([l.name for l in labels])
    context = {
        'labels': labels,
    }
    return render(request, 'app/index.html', context)


def add_label(request, label_name):
    """Add a newly tracked label"""
    label = Label.objects.create(name=label_name, owner=request.user)
    return HttpResponseRedirect(reverse('app:index'))

