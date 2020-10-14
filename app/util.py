import datetime

from django.db.models import Count

from .models import Entry


def most_frequent_entries(user, number=None):
    """
    Retrieve and return the most frequent entries for a given user
    :param user: User for which to select the entries
    :param number: Max number of entries to return. If None, return all
    :return: Dict: Entry name --> frequency (ordered with most frequent entries first)
    """
    entry_counts = Entry.objects.filter(owner=user).values('name').annotate(count=Count('name'))
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