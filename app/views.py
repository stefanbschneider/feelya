import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Entry
from .forms import EntryForm
from .util import most_frequent_entries


logger = logging.getLogger(__name__)


@login_required
def index(request):
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

    # get relevant data
    entries = Entry.objects.filter(owner=request.user).order_by('-date', 'name')
    # construct dict with date --> list of entries; ordered by default in Python 3.6+
    entry_dict = dict()
    for e in entries:
        if e.date in entry_dict:
            entry_dict[e.date].append(e)
        else:
            entry_dict[e.date] = [e]

    entry_counts = most_frequent_entries(request.user, number=30)

    # prepare context
    context = {
        'entry_dict': entry_dict,
        'entry_counts': entry_counts,
        'form': form,
    }

    return render(request, 'app/index.html', context)


@login_required
def add_entry(request, entry_name):
    # only works for post
    if request.method == 'POST':
        entry_name = entry_name.strip().lower()
        entry = Entry.objects.create(name=entry_name, owner=request.user)
    return HttpResponseRedirect(reverse('app:index'))


@login_required
def delete_entry(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=pk, owner=request.user)
        entry.delete()
    else:
        logger.warning(f'delete_query only supports POST requests, got {request.method}')
    return HttpResponseRedirect(reverse('app:index'))


@login_required
def evaluate(request):
    """Eval view that shows how many times each entry was tracked"""
    context = {
        'entry_counts': most_frequent_entries(request.user)
    }
    return render(request, 'app/eval.html', context)
