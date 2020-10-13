from django import forms


class LabelForm(forms.Form):
    label_name = forms.CharField(label='Name of the new label', max_length=100)
