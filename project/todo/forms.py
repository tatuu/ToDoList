from django import forms
from django.db import models
from .models import List, Task

class ListForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': '  リスト名を入力してください'}))

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    deadline_date = forms.DateField(widget=forms.SelectDateWidget)
    text = forms.CharField(max_length=1000, required=False)
        