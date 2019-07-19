from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.utils import timezone
from .models import List
from .forms import ListForm

def index(request):
    form = ListForm(request.POST or None)
    status = False
    if form.is_valid():
        list = List()
        list.title = form.cleaned_data['title']

        List.objects.create(
            title = list.title,
        )
        status = True


    listdata = List.objects.all()
    params = {
        'lists': listdata,
        'form': form,
        'status': status,
    }
    return render(request, 'todo/index.html', params)

def list_new(request):
    form = ListForm(request.POST or None)
    if request.method == 'POST':
        list = List()
        list.title = form.cleaned_data['title']

        List.objects.create(
            title = list.title,
            create_date = models.DateTimeField(default=timezone.now)
        )
    return render(request, 'todo/index.html', {'form': form})



