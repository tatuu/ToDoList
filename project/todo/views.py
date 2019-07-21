from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.utils import timezone
from .models import List, Task
from .forms import ListForm, TaskForm

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

def list(request, list_id):    
    listdata = List.objects.get(id=list_id)
    taskdata = Task.objects.filter(list=listdata)

    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = Task()
        task.title = form.cleaned_data['title']
        task.deadline_date = form.cleaned_data['deadline_date']
        task.text = form.cleaned_data['text']

        Task.objects.create(
            title = task.title,
            deadline_date = task.deadline_date,
            list = listdata,
            text = task.text,
        )

    for t in taskdata:
        if str(t.id) in request.POST:
            if t.completed:
                t.completed = False
            elif not t.completed:
                t.completed = True
            t.save()


    params = {
        'id': list_id,
        'listdata': listdata,
        'taskdata': taskdata,
        'form': form,
    }
    return render(request, 'todo/list.html', params)



