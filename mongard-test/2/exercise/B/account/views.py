from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post
from .models import Relation
from django.contrib.auth import views as auth_views

class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request , 'logout first ...' , 'success')
            return redirect('account:user_register')
        else: # if everything was ok , super() will be passed through get method
            return super().dispatch(request , *args , **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid(): # ^-> now the clean modules will be executed
            try:
                cd = form.cleaned_data
                User.objects.create_user(username=cd['register_form_username'] , email=cd['register_form_email'] , password=cd['register_form_password1'])
                messages.success(request , 'registered successfully ...' , 'success')
                return redirect('home:home')
            except:
                messages.error(request , 'there was a problem in your registeration ... ')
                return render(request , self.template_name , {'form:':form})
        return render(request, 'account/register.html', {'form': form})

########################################################################################################################

class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get['next'] # az onjayi ke omade bargarde masalan az chizi ke LoginRequiredMixin bode
        return super().setup(request , *args , **kwargs)

    def dispath(self , request , *args , **kwargs):
        if request.user.is_authenticated:
            messages.error(request , 'logout first' , 'danger')
            return redirect('account:user_login')

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['login_form_username_or_email'] , password=cd['login_form_password'])
            if user is not None:
                login(request , user)
                messages.success( request , 'loggined ...' , 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request , 'invalid login credentials ... ' , 'danger')
                return render(request , self.template_name , {'form':form})
        else :
            return render(request, 'account/login.html', {'form': form})

########################################################################################################################


class UserLogoutView(LoginRequiredMixin , View):
    def get(self , request):
        try :
            logout(request)
            messages.success(request , 'logged out successfully' , 'success')
            return redirect('home:home')
        except:
            messages.error(request , 'there was a problem in logging you out' , 'daner')
            return redirect('account:user_profile' , request.user.id)

########################################################################################################################


class UserProfileView(LoginRequiredMixin , View):
    template_name = 'account/profile.html'

    def get(self , request , user_id):
        user = get_object_or_404(User , id = user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user= request.user, to_user=user)
        is_following  = False
        if relation.exists():
            is_following = True # if relaton is empty and None , its None so if dosn't work
        return render(request , self.template_name , {'user':user , 'posts':posts , 'is_following':is_following})


########################################################################################################################

class UserFollowingView(LoginRequiredMixin , View):

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(id=kwargs['user_id'])
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.user.id :
            messages.error(request , "you can't follow yourself" , 'danger')
            return redirect('account:user_profile' , self.user.id ) #returning to the wanted user not the loggiend user
        return super().dispatch(request , *args , **kwargs)

    def get(self , requst , *args , **kwargs):

        relation = Relation.objects.filter(from_user=requst.user , to_user=self.user)

        if relation.exists():
            messages.error(requst , 'you already follow this user' , 'danger')
        else:
            Relation(from_user=requst.user , to_user=self.user).save()
            messages.success(requst  , 'you followed him' , 'success')
        return redirect('account:user_profile', self.user.id)

########################################################################################################################

class UserUnFollowingView(LoginRequiredMixin , View):
    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(id=kwargs['user_id'])
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == self.user.id :
            return messages.error(request , 'you cant unfollow your self' , 'danger')
            return redirect('account:user_profile', self.user.id)
        return super().dispatch(request , *args , **kwargs)

    def get(self , request , *args , **kwargs):
        relation = Relation.objects.filter(from_user = request.user , to_user=self.user)

        if relation.exists():
            relation.delete()
            messages.success(request,'you unfollowed him ...' , 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')

        return redirect('account:user_profile', self.user.id)

########################################################################################################################

class PasswordChangeView(auth_views.PasswordResetView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password-reset-email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password-reset-confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password-reset-complete.html'

########################################################################################################################
