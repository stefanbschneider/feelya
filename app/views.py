import logging
import datetime

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Entry
from .forms import EntryForm, PlotForm
from .util import most_frequent_entries, entries_over_time


logger = logging.getLogger(__name__)


@login_required
def index(request, init_date=datetime.date.today()):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            # get the label name and strip and convert to lower before saving it
            entry_name = form.cleaned_data['entry_name'].strip().lower()
            entry_date = form.cleaned_data['entry_date']
            entry = Entry.objects.create(name=entry_name, date=entry_date, owner=request.user)
            return HttpResponseRedirect(reverse('app:index_with_date', args=[entry_date]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = EntryForm(initial={'entry_date': init_date})

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
def add_entry(request, entry_name, entry_date=datetime.date.today()):
    # only works for post
    if request.method == 'POST':
        entry_name = entry_name.strip().lower()
        entry = Entry.objects.create(name=entry_name, date=entry_date, owner=request.user)
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
    # default filter
    end_date = datetime.date.today()
    start_date = datetime.date(year=end_date.year, month=end_date.month - 1, day=end_date.day)
    num_entries = 5

    # get custom filter values from form
    if request.method == 'POST':
        form = PlotForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            num_entries = form.cleaned_data['num_entries']

    # or load empty form
    else:
        form = PlotForm(initial={'start_date': start_date, 'end_date': end_date, 'num_entries': num_entries})

    # prepare chart data
    labels = []
    chart_data = []
    entry_counts = most_frequent_entries(request.user, start_date, end_date, number=num_entries)
    for entry, count in entry_counts.items():
        labels.append(entry)
        chart_data.append(count)

    context = {
        'form': form,
        # for chart.js
        'labels': labels,
        'chart_label': 'Num. Entries',
        'chart_data': chart_data,
        'chart_title': f'Top {num_entries} Most Common Entries',
    }

    return render(request, 'app/eval.html', context)


@login_required
def eval_time_series(request):
    end_date = datetime.date.today()
    start_date = datetime.date(year=end_date.year, month=end_date.month - 1, day=end_date.day)

    # list of all dates between the specified start and end (incl. both)
    delta = end_date - start_date
    str_dates = [str(start_date + datetime.timedelta(days=i)) for i in range(delta.days + 1)]

    # get entries in that time frame as dict of entry names --> list of counts
    entry_dict = entries_over_time(request.user, start_date, end_date)

    example_list = list(entry_dict.values())[0]

    # TODO: get dict of dates from entries_over_time, pass them to the template and visuailze

    context = {
        'dates': str_dates,
        'values': example_list
    }
    return render(request, 'app/eval_time_series.html', context)
