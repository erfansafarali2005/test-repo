from django.shortcuts import render
from django.views import View
from post.models import Post
from .forms import PostSearchForm

class HomeView(View):
    template_name = 'home/home.html'
    form_class = PostSearchForm
    def get(self , request):

        #posts = Post.objects.all().order_by('created')
        posts = Post.objects.all()
        if request.GET.get('search') :
            posts = Post.objects.filter(body__contains=request.GET['search'])
        return render(request , self.template_name , {'posts':posts , 'form':self.form_class})


