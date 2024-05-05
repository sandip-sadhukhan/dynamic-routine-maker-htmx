from django import forms

class RoutineForm(forms.Form):
    name = forms.CharField(max_length=100)
