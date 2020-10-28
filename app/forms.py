import datetime

from django import forms


def last_month():
    today = datetime.date.today()
    return datetime.date(year=today.year, month=today.month - 1, day=today.day)


class EntryForm(forms.Form):
    entry_name = forms.CharField(label='New Entry', max_length=100)
    entry_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class PlotForm(forms.Form):
    num_entries = forms.IntegerField(label='Number of different entries to display', max_value=30, min_value=1)
    start_date = forms.DateField(initial=last_month, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date must not be before end date.")

    # def clean_start_date(self):
    #     start_date = self.cleaned_data['start_date']
    #     end_date = self.cleaned_data['end_date']
    #     if start_date > end_date:
    #         raise forms.ValidationError("Start date must not be before end date.")
    #     return start_date
