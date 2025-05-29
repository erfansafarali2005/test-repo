from pyexpat.errors import messages
from django.shortcuts import render, redirect , get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm , CommentCreateForm , CommentReplyForm
from .models import Post , Comment
from django.contrib import messages

class PostCreateView(LoginRequiredMixin , View):
    template_name = 'post/create.html'
    form_class = PostCreateUpdateForm

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                cd = form.cleaned_data
                new_post = form.save(commit=False)
                new_post.slug = slugify(cd['body'][:30])
                new_post.user = request.user
                new_post.save()
                messages.success(request , 'post created successfully' , 'success')
                return redirect('account:user_profile' , request.user.id)
            except:
                messages.error(request , 'there was a problem in creating your post' , 'danger')
                return render(request , self.template_name , {'form':form})

############################################################################################################################

class PostDetailView(View):
    template_name = 'post/detail.html'
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post , id=kwargs['post_id'] , slug=kwargs['post_slug'])
        return super().setup(request , args , kwargs)

    def get(self, request, post_id , post_slug):
        #post = Post.objects.get(id=post_id , slug=post_slug)
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, self.template_name , {'post': self.post_instance , 'comments':comments , 'form':self.form_class, 'reply_form':self.form_class_reply,})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect('post:post_detail', self.post_instance.id, self.post_instance.slug)

############################################################################################################################


class PostDeleteView(LoginRequiredMixin , View):
    def get(self , request , post_id):
        post = get_object_or_404(Post , pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , 'post delete d sucesffully' , 'success')
        else:
            messages.danger(request , 'post could not be deleted , you can delete only your posts' , 'danger')
        return redirect("home:home")

############################################################################################################################


class PostUpdateView(LoginRequiredMixin , View):
    template_name = 'post/update.html'
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request , *args , **kwargs)

    def dispatch(self , request , *args , **kwargs):
        if request.user.id != self.post_instance.user.id :
            messages.error(request , 'you only can update your own posts' , 'danger')
            return redirect(request, 'home:home')
        return super().dispatch(request , *args , **kwargs)

    def get(self , request , *args , **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request , self.template_name , {'form':form})

    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST , instance=self.post_instance)
        if form.is_valid():
            cd = form.cleaned_data
            updated_post = form.save(commit=False)
            updated_post.slug = slugify(cd['body'][:30])
            updated_post.save()
            messages.success(request, 'succesfully updated your post', 'success')
            return redirect('post:post_detail', self.post_instance.id, self.post_instance.slug)

        return  render(request , self.template_name,{'form':form})

############################################################################################################################


class PostAddReplyView(View):
    form = CommentReplyForm

    def post(self , request , post_id , comment_id):
        form = self.form(request.POST)
        post = get_object_or_404(Post , id = post_id)
        comment = get_object_or_404(Comment , id = comment_id)

        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.post = post
            new_reply.reply = comment
            new_reply.user = request.user
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
        return redirect('post:post_detail', post.id, post.slug)


############################################################################################################################