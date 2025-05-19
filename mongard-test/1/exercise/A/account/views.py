from django.shortcuts import render, redirect
from .forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def user_register(request):
    template_name = 'user_register.html'
    if request.method == 'GET':
        form = UserRegisterationForm()
        return render(request, template_name , {'form':form})
    else:
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
                messages.success(request, 'Account created successfully' , 'success')
                return redirect('home:home')
            except:
                messages.error(request, 'Account creation failed' , 'error')
                return render(request, template_name , {'form':form})

        return render(request, template_name , {'form':form})

def user_login(request):
    template_name = 'user_login.html'
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, template_name , {'form':form})
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account logged successfully' , 'success')
                    return redirect('home:home')

            except:
                messages.error(request, 'Account login failed' , 'error')
                return render(request, template_name , {'form':form})
        else:
            return render(request, template_name , {'form':form})

def user_logout(request):
    try:
        logout(request)
        messages.success(request, 'User logged out successfully' , 'success')
        return redirect('home:home')
    except:
        messages.error(request, 'User logout failed' , 'error')
        return render('home:home')


