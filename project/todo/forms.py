from django import forms
from django.db import models

class ListForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': '  リスト名を入力してください'}))