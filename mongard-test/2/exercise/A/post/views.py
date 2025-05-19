from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect , get_object_or_404
from django.utils.text import slugify
from django.views import View
from .models import Post
from django.contrib.auth.models import User
from .forms import PostCreateForm , PostUpdateForm
from django.contrib import messages

class PostCreateView(LoginRequiredMixin , View):
    template_name = 'post/post_create.html'
    form_class = PostCreateForm

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.slug = slugify(cd['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request , 'post created successfully' , 'success')
            return redirect('home:home')
        else:
            return render(request , self.template_name , 'success' )

####################################################################################################################

class PostDetailView(View):
    template_name = 'post/post_detail.html'
    def get(self , request , post_id , post_slug):
     post = Post.objects.get(id=post_id , slug=post_slug)
     return render(request , self.template_name , {'post':post})

####################################################################################################################

class PostDeleteView(LoginRequiredMixin,View):
    def get(self , request , post_id):
        try :
             post = Post.objects.get(id=post_id)
             post.delete()
             messages.success(request , 'post deleted successfully' , 'success')
             return redirect('account:user_profile')
        except :
            messages.error(request,'there was a problem in deleting your post , please try again later ...' , 'error')
            return redirect('post:post_detail' , post.id)

####################################################################################################################

class PostUpdateView(LoginRequiredMixin , View):
    template_name = 'post/post_update.html'
    form_class = PostUpdateForm

    def setup(self , request , *args , **kwargs):
        self.post_instance = get_object_or_404(Post , pk=kwargs['post_id'])
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.post_instance.user.id :
            messages.error(request , 'you cant edit posts which you are not their admin ..' , 'error')
            return redirect('post:post_detail' , self.post_instance.id , self.post_instance.slug)
        return super().dispatch(request , *args , **kwargs)

    def get(self , request , *args , **kwargs): # we must give it **kwargs or post.id becaseu it needs it but we don't need it in get
        form = self.form_class(instance=self.post_instance)
        return render(request , self.template_name , {'form':form})

    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST , instance = self.post_instance)

        if form.is_valid():
            try:
                updated_post = form.save(commit=False)
                updated_post.slug = slugify(form.cleaned_data['body'][:30])
                updated_post.save()
                messages.success(request , 'post updated successfully' , 'success')
                return redirect('post:post_detail' , updated_post.id , updated_post.slug)
            except Exception as e :
                print(e)
                messages.error(request , 'there was a problem with updating your post ...' , 'danger')

        return render(request , self.template_name , {'form' : form})


####################################################################################################################