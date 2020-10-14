from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Entry
from .forms import EntryForm


def index(request):
    entries = Entry.objects.order_by('-date')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            # get the label name and strip and convert to lower before saving it
            entry_name = form.cleaned_data['entry_name'].strip().lower()
            entry = Entry.objects.create(name=entry_name, owner=request.user)
            return HttpResponseRedirect(reverse('app:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EntryForm()

    # prepare context
    context = {
        'entries': entries,
        'form': form
    }

    return render(request, 'app/index.html', context)
