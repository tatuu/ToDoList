from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<int:list_id>', views.list, name="list"),
    path('task/<int:task_id>', views.task, name="task"),
    path('search', views.search, name="search"),
    path('search_result/', views.search_result, name="search_result"),
]