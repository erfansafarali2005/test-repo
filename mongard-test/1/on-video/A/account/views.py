from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .forms import UserRegisterationForm , UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def user_register(request):
    template_name = 'register.html'
    form = UserRegisterationForm()
    if request.method == 'GET':
        return render(request , template_name , {'form': form} )
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
                return render(request , template_name , {'form': form} )
        return render(request, template_name, {'form': form})

def user_login(request):
    template_name = 'login.html'

    if request.method == 'GET':
        form = UserLoginForm()
        return render(request , template_name , {'form': form} )
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account logged successfully' , 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'Invalid username or password', 'error')
                    return render(request , template_name , {'form': form} )
            except:
                messages.error(request, 'Account login failed' , 'error')
                return render(request , template_name , {'form': form})
        return render(request, template_name, {'form': form})


def user_logout(request):
    
        try:
            logout(request)
            messages.success(request, 'You have been logged out' , 'success')
        except:
            messages.error(request, 'You have been logged out' , 'error')
            return render('home:home')
        return redirect('home:home')

