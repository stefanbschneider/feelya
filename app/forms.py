from django import forms


class EntryForm(forms.Form):
    entry_name = forms.CharField(label='New Entry', max_length=100)
