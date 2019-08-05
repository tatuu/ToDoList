from django import forms
from django.db import models
from .models import List, Task

class ListForm(forms.Form):
    title = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'リスト名を入力してください'}))

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'ToDo名を入力してください'}))
    deadline_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    text = forms.CharField(max_length=1000, required=False, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'メモを入力できます'}))
        