from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm , UserLoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout

class UserRegisterView(View):
    template_name = 'account/user_register.html'
    form_class = UserRegisterationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request , 'you are loggged in , log out first to register' , 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['form_register_username'] , email=cd['form_register_email'] , password=cd['form_register_password1'])
            messages.success(request , 'registeration successfull welcome to our company' , 'success')
            return redirect('home:home')
        return render(request , self.template_name , {'form':form})

########################################################################################################################

class UserLoginView(View):
    template_name = 'account/user_login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        print("Dispatch called - Authenticated:", request.user.is_authenticated)  # Debug
        if request.user.is_authenticated:
            messages.error(request , 'you are already logged in , no need for loggin again ' , 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})


    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['form_login_username'], password=cd['form_login_password'])
            if user is not None:
                login(request , user)
                messages.success(request , 'loggined successfully ...' , 'success')
                return redirect('home:home')
            else:
                messages.error(request , 'username or password is wrong ...' , 'error')
                return render(request, self.template_name, {'form': form})


        else:
            return render(request , self.template_name , {'form':form})

########################################################################################################################

class UserLogoutView(LoginRequiredMixin , View):
    def get(self , request):
        try:
            logout(request)
            messages.success(request , 'logged out successfully' , 'success')
            return redirect('home:home')
        except:

            messages.error(request , 'there was a problem is your logging out ...' , 'danger')
            return render(request , 'account/user_profile.html')

########################################################################################################################

class UserProfileView(LoginRequiredMixin , View):
    template_name = 'account/user_profile.html'
    def get(self , request , **kwargs):
        try :
            user = User.objects.get(id=kwargs['user_id'])
            return render(request , self.template_name , {'user':user})
        except:
            print(e)
            messages.error(request , 'there was a problem in showing your profile pelase try again ...' , 'error')
            return redirect('home:home')

########################################################################################################################