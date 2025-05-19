from django.urls import path
from . import views

app_name='todo'

urlpatterns = [
    path('create/' , views.create_todo , name='create_todo'),
    path('detail/<int:todo_id>' , views.todo_detail , name='todo_detail'),
    path('delete/<int:todo_id>' , views.todo_delete , name='todo_delete'),
    path('update/<int:todo_id>' , views.todo_update , name='todo_update')

]