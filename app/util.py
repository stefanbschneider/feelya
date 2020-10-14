import datetime


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