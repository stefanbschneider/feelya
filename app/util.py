import datetime

from django.db.models import Count

from .models import Entry


today = datetime.date.today()
last_week = today - datetime.timedelta(weeks=1)
last_year = today - datetime.timedelta(days=365)


def list_of_colors(length):
    """Return a list of colors of the given length"""
    # list of nice colors: https://coolors.co/f94144-f3722c-f8961e-f9c74f-90be6d-43aa8b-577590
    base_colors = ['#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d', '#43aa8b', '#577590']

    colors = []
    for i in range(length):
        colors.append(base_colors[i % len(base_colors)])
    return colors


def entries_over_time(user, start_date=last_week, end_date=today):
    """
    Retrieve and return all entries for a given user over time within a given time frame

    :param user: User for which to get the entries
    :param start_date: Start date from where to start getting entries
    :param end_date: End date until when to get entries
    :return: Dict: Entry name --> list of entry counts per day within the time frame (one element per day)
    """
    # list of all dates between the specified start and end (incl. both)
    delta = end_date - start_date
    dates = [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]

    # get all values for the user in this time frame ordered by increasing date
    entries = Entry.objects.filter(owner=user, date__gte=start_date, date__lte=end_date).order_by('-date')

    # construct dict with entry name --> list of counts per day
    entry_dict = dict()
    for e in entries:
        # initialize with list of zeros for the time frame
        if e.name not in entry_dict:
            entry_dict[e.name] = [0 for _ in range(len(dates))]
        # then increment count at the corresponding date
        idx = (e.date - start_date).days
        entry_dict[e.name][idx] += 1

    return entry_dict


def most_frequent_entries(user, start_date=last_year, end_date=today, number=None):
    """
    Retrieve and return the most frequent entries for a given user
    :param user: User for which to select the entries
    :param number: Max number of entries to return. If None, return all
    :return: Dict: Entry name --> frequency (ordered with most frequent entries first)
    """
    entry_counts = Entry.objects.filter(owner=user, date__gte=start_date, date__lte=end_date)\
        .values('name').annotate(count=Count('name'))
    # sort with decreasing frequency
    counts_sorted = sorted(entry_counts, key=lambda e: e['count'], reverse=True)
    # slice according to given max number
    if number is not None:
        counts_sorted = counts_sorted[:number]
    entry_dict = {e['name']: e['count'] for e in counts_sorted}
    return entry_dict


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