from django.contrib.auth.models import User
from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation

class UserRegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Account already logged in , please logout first' , 'info')
            return redirect('home:home')
        return super().dispatch(request , *args , **kwargs) # if everythign was ok and if dosn't work , it retuns all data to get .


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name , {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid(): #valid calls the clean and clean_email and clean_username from forms.py
            try:
                cd = form.cleaned_data
                User.objects.create_user(username=cd['username'], email=cd['email'], password1=cd['password1'] , password2=cd['password2'])
                messages.success(request, 'Account created successfully' , 'success')
                return redirect('home:home')
            except Exception as e:
                print(e)
                messages.error(request, 'Account creation failed' , 'error')
                return render(request, 'account/register.html', {'form': form})

        return render(request, 'account/register.html', {'form': form})

########################################################################################################################

class UserLoginView(View):
    template_name = 'account/login.html'
    form = UserLoginForm

    def setup(self , request , *args , **kwargs):
        self.next = request.Get.get('next') # if its empty it returns None
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Account already logged in logout first' , 'info')
            return redirect('home:home')
        return super().dispatch(request , *args , **kwargs) # if everythign was ok and if dosn't work , it retuns all data to get .

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None : # is not none : means it checks if its none or a user , but if user : also wont start if we have False and emty None thing
                login(request, user)
                messages.success(request, 'Account logged in' , 'success')
                if self.next: # if next was empty it returns None
                    return redirect(self.next)
                return redirect('home:home')
            else: # when we have else so we don't need user is not None , if user is enough
                messages.error(request, 'Account login failed' , 'error')
                return render(request, 'account/login.html', {'form': form})

        return render(request, 'account/login.html', {'form': form})

########################################################################################################################

class UserLogoutView(LoginRequiredMixin,View):
    #LOGIN_URL = '/account/login/' here or in setting
    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out' , 'success')
        return redirect('home:home')


########################################################################################################################

class UserProfileView( LoginRequiredMixin , View):
    template_name = 'account/profile.html'

    def get(self , request , user_id):
        #user = User.objects.get(id=user_id)
        user = get_object_or_404(User , id=user_id) #if user dosn't now exists it shows 404
        #posts = Post.objects.filter(user=user)
        posts = user.posts.all()
        is_following = False
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request, self.template_name, {'user': user , 'posts': posts , 'is_following':is_following})

########################################################################################################################

class UserPasswordResetView(auth_views.PasswordResetView): #main class of the overal and main settings of reset passwrod
    template_name = 'account/password_reset_form.html'
    success_url =  reverse_lazy('account:password_reset_done')   #everything has done , so where do i need to redirect the user
                    # ^-> if we use reverse , becasue of that in the beninging of the project the done view url is not generated it retunrs error
    email_template_name = 'account/password_reset_email.html' #the html email content

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView): #where it says the link is sent
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView): # where user enters its new password
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete') # redirects to the page that says your password is changed successfully

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

########################################################################################################################

class UserFollowView(LoginRequiredMixin , View):
    def get(self , request , user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request , 'you are already following this user' , 'danger')
        else:
            Relation.objects.create(from_user = request.user , to_user = user)
            messages.success(request , 'followed successfully' , 'success')
        return redirect('account:user_profile' , user.id)


class UserUnFollowView(LoginRequiredMixin , View):
    def get(self , request , user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.id , to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request , 'you unfollowed this user' , 'success')
        else:
            messages.error(request , 'you are not following this user' , 'danger')

        return redirect('account:user_profile' , user.id)