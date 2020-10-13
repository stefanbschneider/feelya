from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Label
from .forms import LabelForm


def index(request):
    labels = Label.objects.order_by('-date')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = LabelForm(request.POST)

        if form.is_valid():
            # process as needed
            label = Label.objects.create(name=form.cleaned_data['label_name'], owner=request.user)
            return HttpResponseRedirect(reverse('app:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LabelForm()

    # prepare context
    context = {
        'labels': labels,
        'form': form
    }

    return render(request, 'app/index.html', context)
