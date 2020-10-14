import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Entry
from .forms import EntryForm


def order_entries(entries, last_days=7):
    """
    Order the given entries by date and return a dict that has a key for the last last_days days.
    Each key points to a (possibly empty) list of entries of that day
    """
    today = datetime.date.today()
    days = [today - datetime.timedelta(days=i) for i in range(last_days)]
    # construct dict with empty list for each day
    entry_dict = {day: [] for day in days}
    # fill it by iterating over the list of given entries
    for e in entries:
        if e.date in entry_dict:
            entry_dict[e.date].append(e)
    return entry_dict


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
