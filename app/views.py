from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Entry
from .forms import EntryForm


@login_required
def index(request):
    entries = Entry.objects.filter(owner=request.user).order_by('-date', 'name')
    # tracked_dates = Entry.objects.values('date').distinct()
    # construct dict with date --> list of entries; ordered by default in Python 3.6+
    entry_dict = dict()
    for e in entries:
        if e.date in entry_dict:
            entry_dict[e.date].append(e)
        else:
            entry_dict[e.date] = [e]

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
        # 'entries': entries,
        'entry_dict': entry_dict,
        # 'dates': tracked_dates,
        'form': form,
    }

    return render(request, 'app/index.html', context)


@login_required
def evaluate(request):
    # returns a QuerySet/list of dicts with 'name' and 'count'
    entry_counts = Entry.objects.filter(owner=request.user).values('name').annotate(count=Count('name'))
    # sort with decreasing frequency
    counts_sorted = sorted(entry_counts, key=lambda e: e['count'], reverse=True)
    count_strings = [f"{e['count']}x: {e['name']}" for e in counts_sorted]
    context = {
        'entry_counts': counts_sorted,
        'count_strings': count_strings,
    }
    return render(request, 'app/eval.html', context)
