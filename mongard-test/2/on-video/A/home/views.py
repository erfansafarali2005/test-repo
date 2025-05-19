from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render , get_object_or_404 , redirect
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from .models import Post , Comment
from django.contrib import messages
from .forms import PostCreateUpdateForm , PostSearchForm , CommentCreateForm , ReplyCommentForm


class HomeView(View):
    template_name = 'home/home.html'
    form_class = PostSearchForm

    def get(self, request):
        #posts = Post.objects.all()
        posts = Post.objects.all().order_by('created')
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, self.template_name , {'posts': posts , 'form':self.form_class})



###################################################################################################

class PostDetailView(View):
    template_name = 'home/post_detail.html'
    form_class = CommentCreateForm
    form_class_reply = ReplyCommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'] , slug=kwargs['post_slug'])
        return super().setup(request , *args , **kwargs)

    def get(self, request ,*args , **kwargs):
        post = self.post_instance
        comments = post.pcomments.filter(is_reply = False)
        form = self.form_class()
        form_reply = self.form_class_reply

        return render(request, self.template_name , {'post': post , 'comments':comments , 'form':form ,
                                                     'reply_form' : form_reply})

    @method_decorator(login_required)
    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.usesr
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request , 'your comment commited successfully' , 'success')
            return redirect('home:post_detail' , self.post_instance.id , self.post_instance.slug)

###################################################################################################

class PostDeleteView(LoginRequiredMixin , View):
    def get(self , request , post_id):
        post = get_object_or_404(Post , pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , 'post delete d sucesffully' , 'success')
        else:
            messages.danger(request , 'post could not be deleted' , 'danger')
        return redirect("home:home")
###################################################################################################

class PostUpdateView(LoginRequiredMixin , View):
    template_name = 'home/post_update.html'
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs): #it saves the all data that we need to prevent looping through the database
        self.post_instance = get_object_or_404(Post , pk=kwargs['post_id'])
        #self.post_instance = Post.objects.get(pk=kwargs['post_id']) #is saved in self to be used on other methods
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        #post = Post.objects.get(pk=kwargs['post_id'])
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request , 'you cant update this post')
            return redirect(request , 'home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(instance=post)
        return  render(request , self.template_name,{'form':form})
        #if not post.user.id == request.user.id:
            #messages.error(request , 'you cant update this post')
            #return redirect(request , 'home:home')

    def post(self,request,*args , **kwargs):
        #post = Post.objects.get(pk=post_id)
        post = self.post_instance
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request , 'succesfully updated your post' , 'success')
            return redirect('home:post_detail', post.id, post.slug)
        return  render(request , self.template_name,{'form':form})
        #post = Post.objects.get(pk=post_id)
        #if not post.user.id == request.user.id:
            #messages.error(request , 'you cant update this post')
            #return redirect(request , 'home:home')

###################################################################################################

class PostCreateView(LoginRequiredMixin , View):
    form_class = PostCreateUpdateForm
    template_name = 'home/post_create.html'
    def get(self , request , *args , **kwargs):
        form = self.form_class
        return render(request , self.template_name , {'form' : form})
    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST) #request.post  : data coming from POST
        if form.is_valid():
            new_post = form.save(commit=False) #we did these because we need to creare the slug for it
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request , 'you have successfully created  a new post' , 'success')
            return redirect('home:post_detail' , new_post.id , new_post.slug)


###################################################################################################

class PostAddReplyView(LoginRequiredMixin , View):
    form_class = ReplyCommentForm

    def post(self , request , post_id , comment_id):
        post = get_object_or_404(Post , id = post_id)
        comment = get_object_or_404(Comment , id = comment_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            form.save()
            messages.success(request , 'reply added successfully' , 'success')
        return redirect('home:post_detail' , post.id , post.slug)

###################################################################################################