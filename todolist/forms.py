from django import forms
from .models import Todolist, Share
from django.forms import ModelForm
from django.forms import formset_factory

class TodolistForm(ModelForm):

    class Meta:
        model = Todolist
        fields = ['name', 'description', 'end_date']
        widgets = {
            'end_date': forms.TextInput(attrs={'id': 'datetimepicker'}),
        }


class ShareForm(ModelForm):

    class Meta:
        model = Share
        fields = ['todoer', 'type']

    Choices = (
        ("0", "View only"),
        ("1", "Can Comment"),

    )
    todoer = forms.CharField(required=True, max_length=255, label="Email or username")
    type = forms.ChoiceField(required=True, choices=Choices, widget=forms.RadioSelect())
