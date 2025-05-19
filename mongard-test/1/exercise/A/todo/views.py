from django.shortcuts import render, redirect , HttpResponse
from .models import Todo
from .forms import TodoCreationForm , TodoUpdateForm
from django.contrib import messages

def create_todo(request):
    template_name = 'todo_create.html'
    if request.method == 'GET':
        form = TodoCreationForm()
        return render(request, template_name , {'form': form})
    else:
        form = TodoCreationForm(request.POST)

        if form.is_valid():
            try:
                cd = form.cleaned_data
                Todo.objects.create(title=cd['title'] , body=cd['body'])
                messages.success(request, 'Task created successfully' , 'success')
                return redirect('home:home')
            except Exception as e:
                print(e)
                messages.error(request, 'Something went wrong' , 'error')
                return render(request, template_name , {'form': form})

        else:
            return render(request, template_name , {'form': form})


def todo_detail(request , todo_id):
    template_name = 'todo_detail.html'
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'GET':
        return render(request, template_name , {'todo':todo})
    else:
        return redirect('home:home')

def todo_delete(reqeust , todo_id):
    if reqeust.method == 'get':
        return HttpResponse('not accepted')
    else:
        todo = Todo.objects.get(id=todo_id).delete()
        messages.success(reqeust , 'you deleted todo successfully' , 'success')
        return redirect('home:home')


def todo_update(request , todo_id):
    template_name = 'todo_update.html'
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'GET':
        form = TodoUpdateForm(instance=todo)
        return render(request , template_name , {'form':form})
    else :
        form = TodoUpdateForm(request.POST , instance=todo)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Task updated successfully' , 'success')
                return redirect('todo:todo_detail' , todo.id)
            except:
                messages.error(request, 'Something went wrong' , 'error')
                return render(request , template_name , {'form':form})
        return render(request , template_name , {'form':form})