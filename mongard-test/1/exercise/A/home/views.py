from django.shortcuts import render
from todo.models import Todo

def home_view(request):
    template_name = 'home.html'
    if request.method == "GET":
        todos = Todo.objects.all()
        return render(request, template_name , {'todos':todos})
    else:
        pass
