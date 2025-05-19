from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Todo
from django.contrib import messages
from .forms import TodoCreateForm, TodoUpdateForm


def home(request):
    template_name = 'home.html' # templates/home.html is not ok . templates is added in setting.py
    #person = {'name' : 'erfan'}
    todos = Todo.objects.all()
    return render(request , template_name , {'todos':todos}) # in html :  user.name , user is passed not person

def todo_detail(request , **kwargs):
    template_name = 'detail.html'
    print(kwargs)
    #todo = Todo.objects.get(id=todo_id)
    todo = Todo.objects.get(id=kwargs['todo_id'])
    return render(request , template_name , {'todo' : todo})

def todo_delete(reqeust , todo_id):
    if reqeust.method == 'get':
        return HttpResponse('not accepted')
    else:
        todo = Todo.objects.get(id=todo_id).delete()
        messages.success(reqeust , 'you deleted todo successfully' , 'success')
        return redirect('home:home')

def create_todo_html(request):
    template_html_name = 'create-html.html'
    if request.method == 'GET':
        return render(request , template_html_name)
    else:
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            Todo.objects.create(title=title , body=description)
            messages.success(request , 'your todo created succeessfully' , 'success')
            return redirect('home:home')
        except:
            messages.error(request , 'not valid' , 'danger')
            return render(request , template_html_name)

def create_todo(request):
    template_name = 'create.html'
    if request.method == 'GET':
        form = TodoCreateForm()

        return render(request , template_name , {'form': form})
    else:
        form = TodoCreateForm(request.POST) #things are put here
        if form.is_valid():
            cd = form.cleaned_data
            try:
                Todo.objects.create(title=cd['title'] , body=cd['body'])
                messages.success(request , 'your todo created succeessfully' , 'success')
                return redirect('home:home')
            except:
                messages.error(request , 'not valid' , 'danger')
                return render(request , template_name)

def update_todo(request,todo_id):
    todo = Todo.objects.get(id=todo_id)
    template_name = 'update.html'
    if request.method == 'GET':
        form = TodoUpdateForm(instance=todo) # the previous data to be shown
        return render(request , template_name , {'form': form})
    else:
        form = TodoUpdateForm(request.POST , instance=todo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'your todo updated succeessfully', 'success')
                return redirect('home:home')
            except:
                messages.error(request , 'not valid' , 'danger')
                return render(request , template_name , {'form': form})
