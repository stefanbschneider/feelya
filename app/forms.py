import datetime

from django import forms


class EntryForm(forms.Form):
    entry_name = forms.CharField(label='New Entry', max_length=100)
    entry_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class PlotForm(forms.Form):
    num_entries = forms.IntegerField(label='Number of entries to display', max_value=30, min_value=1)
