from django.urls import path
from . import views

app_name = 'home' #its needed

urlpatterns = [
    path('',views.home , name='home'),
    path('detail/<int:todo_id>' , views.todo_detail , name='detail'),
    path('delete/<int:todo_id>' , views.todo_delete , name='delete'),
    path('create-html/' , views.create_todo_html , name='create_todo_html'),
    path('create/' , views.create_todo , name='create'),
    path('update/<int:todo_id>' , views.update_todo , name='update')
]