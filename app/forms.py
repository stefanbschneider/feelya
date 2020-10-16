import datetime

from django import forms


class EntryForm(forms.Form):
    entry_name = forms.CharField(label='New Entry', max_length=100)
    entry_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
