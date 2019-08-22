from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import List, Task
from .forms import ListForm, TaskForm
import collections as cl
import html

def index(request):
    listdata = List.objects.all()
    making_list = True
    for l in listdata:
        if 'delete_' + str(l.id) in request.POST:
            l.delete()
            listdata = List.objects.all()
            making_list = False
            break

    form = ListForm(request.POST or None)
    status = False  #Trueならば「新しいToDoリストが作成されました」の表示
    if making_list:
        if form.is_valid(): #リストの作成
            list = List()
            list.title = form.cleaned_data['title']

            if len(list.title) >= 30:
                form.add_error(None, 'ToDoリストの名称は30文字以内にしてください')
            elif len(list.title) == 0:
                form.add_error(None, 'ToDoリストの名称を入力してください')
            else:
                List.objects.create(
                    title = html.escape(list.title),
                )
                status = True
                form = ListForm() #ページ遷移後のformの入力値(value)をクリア


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

    status = False  #Trueならば「新しいToDoが作成されました」の表示

    create_task = True
    form = TaskForm(request.POST or None)


    for t in taskdata:
        if 'status_' + str(t.id) in request.POST:
            if t.completed:
                t.completed = False
            elif not t.completed:
                t.completed = True
            t.save()
            break
        elif 'delete_' + str(t.id) in request.POST:
            t.delete()
            taskdata = Task.objects.filter(list=listdata)
            break

    
    if form.is_valid():
        if len(form.cleaned_data['title']) >= 30:
            form.add_error(None, 'ToDo名が31文字以上入力されています')
            create_task = False

        escape_title = html.escape(form.cleaned_data['title'])
        for t in taskdata:
            if t.title == escape_title:
                form.add_error(None, '同じToDo名のタスクが既に存在します')
                create_task = False
                break
        
        task = Task()
        task.title = escape_title
        task.deadline_date = form.cleaned_data['deadline_date']
        task.text = html.escape(form.cleaned_data['text'])

        if create_task:
            Task.objects.create(
                title = task.title,
                deadline_date = task.deadline_date,
                list = listdata,
                text = task.text,
            )
            status = True
            form = TaskForm() #ページ遷移後のformの入力値(value)をクリア

    
    sort_target = 'deadline_date'
    order_sort_target = 'deadline_date'
    sort = 'ascending'
    if 'sort_task' in request.POST:
        sort1 = request.POST.get('sort1')
        sort2 = request.POST.get('sort2')
        
        if sort1 == '作成日':
            sort_target = 'create_date'
        elif sort1 == '期限':
            sort_target = 'deadline_date'

        if sort2 == '降順':
            order_sort_target = '-' + sort_target
            sort = 'descending'
        elif sort2 == '昇順':
            order_sort_target = sort_target
            sort = 'ascending'

    taskdata = Task.objects.filter(list=listdata).order_by(order_sort_target)#タスクの追加や削除、変更の反映の為にもう一度代入
            

    params = {
        'id': list_id,
        'listdata': listdata,
        'taskdata': taskdata,
        'form': form,
        'status': status,
        'sort_target': sort_target,
        'sort': sort,
    }
    return render(request, 'todo/list.html', params)

def task(request, task_id):
    taskdata = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None)

    def check_task(title):
        if len(title) >= 30:
            form.add_error(None, 'ToDo名が31文字以上入力されています')
            return False

        td = Task.objects.filter(list=taskdata.list)
        escape_title = html.escape(title)
        for t in td:
            if t.id == task_id:
                continue #同じToDoの時のみ
            if t.title == escape_title:
                form.add_error(None, '同じToDo名のタスクが既に存在します')
                return False

        return True

    if form.is_valid():
        check_title = form.cleaned_data['title']
        if check_task(check_title):
            taskdata.title = html.escape(check_title)
            taskdata.deadline_date = form.cleaned_data['deadline_date']
            taskdata.text = html.escape(form.cleaned_data['text'])
            taskdata.save()
            messages.success(request, '編集内容を保存しました')
    else:
        form = TaskForm(initial = {
            'title': taskdata.title,
            'deadline_date': taskdata.deadline_date,
            'text': taskdata.text,
        })

    params = {
        'form' : form,
        'taskdata' : taskdata,
    }

    return render(request, 'todo/task.html', params)

def search(request):
    return render(request, 'todo/search.html')

def search_result(request):    
    input_text = request.GET.get("title")

    ls = cl.OrderedDict()
    ts = cl.OrderedDict()
    tx = cl.OrderedDict()

    if input_text:
        count = 0
        for l in List.objects.filter(title__icontains=input_text):
            ls[count] = cl.OrderedDict({"id":l.id, "title": l.title, "create_date": "{0:%Y年%m月%d日}".format(l.create_date)})
            count += 1

        count = 0
        for t in Task.objects.filter(title__icontains=input_text):
            ts[count] = cl.OrderedDict({"list_id":t.list.id, "list_title":t.list.title, "title":t.title, "create_date":"{0:%Y年%m月%d日}".format(t.create_date), "deadline_date":"{0:%Y年%m月%d日}".format(t.deadline_date)})
            count += 1

        count = 0
        for t in Task.objects.filter(text__icontains=input_text):
            tx[count] = cl.OrderedDict({"list_id":t.list.id, "list_title":t.list.title, "title":t.title, "text":t.text, "create_date":"{0:%Y年%m月%d日}".format(t.create_date), "deadline_date":"{0:%Y年%m月%d日}".format(t.deadline_date)})
            count += 1

    params = {
        'list': ls,
        'task': ts,
        'text': tx,
    }

    return JsonResponse(params)