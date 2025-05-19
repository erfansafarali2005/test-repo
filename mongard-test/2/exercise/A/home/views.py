from django.shortcuts import render
from django.views import View
from post.models import Post



class HomeView(View):

    template_name = 'home/home.html'

    def get(self , request):
        posts = Post.objects.all()
        return render(request , self.template_name , {'posts' : posts})



####################################################################################################################

