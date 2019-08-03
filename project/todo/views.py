from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .models import List, Task
from .forms import ListForm, TaskForm
import collections as cl

def index(request):
    form = ListForm(request.POST or None)
    status = False  #Trueならば「新しいToDoリストが作成されました」の表示
    if form.is_valid(): #リストの作成
        list = List()
        list.title = form.cleaned_data['title']

        List.objects.create(
            title = list.title,
        )
        status = True


    listdata = List.objects.all()
    taskdata = Task.objects.all()

    dict_num = {}
    dict_checked_num = {}
    dict_deadline = {}
    for l in listdata:
        task_num = 0
        checked_task_num = 0
        closest_deadline = None
        for t in taskdata:
            if l == t.list:
                task_num += 1   #タスク数の加算
                if t.completed:
                    checked_task_num += 1   #チェック済みタスク数の加算
                else:
                    if closest_deadline is None or closest_deadline >= t.deadline_date:
                        closest_deadline = t.deadline_date  #もっとも近い締切がNoneまたは比較対象のほうが近い締切ならば代入

        if closest_deadline is not None:
            closest_deadline = "{0:%Y年%m月%d日}".format(closest_deadline)
        
        dict_num[l.id] = task_num
        dict_checked_num[l.id] = checked_task_num
        dict_deadline[l.id] = closest_deadline

    params = {
        'lists': listdata,
        'tasks': taskdata,
        'form': form,
        'status': status,
        'dict_num': dict_num,
        'dict_checked_num': dict_checked_num,
        'dict_deadline': dict_deadline,
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

def search(request):
    return render(request, 'todo/search.html')

def search_result(request):    
    input_text = request.GET.get("title")

    ls = cl.OrderedDict()
    ts = cl.OrderedDict()


    if input_text:
        count = 0
        for l in List.objects.filter(title__icontains=input_text):
            ls[count] = cl.OrderedDict({"id":l.id, "title": l.title, "create_date": "{0:%Y年%m月%d日}".format(l.create_date)})
            count += 1

        count = 0
        for t in Task.objects.filter(title__icontains=input_text):
            ts[count] = cl.OrderedDict({"list_id":t.list.id, "list_title":t.list.title, "title":t.title, "create_date":"{0:%Y年%m月%d日}".format(t.create_date), "deadline_date":"{0:%Y年%m月%d日}".format(t.deadline_date)})
            count += 1

    params = {
        'list': ls,
        'task': ts,
    }

    return JsonResponse(params)