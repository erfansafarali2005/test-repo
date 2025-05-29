from django.contrib import messages
from django.shortcuts import render, redirect , Http404
from django.views import View
from .forms import UserRegisterationForm , VefiyCodeForm
import random
from utils import send_otp_code
from .models import OTPCode , User

class UserRegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserRegisterationForm


    def get(self , request ,  *args , **kwargs):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone_number'] , random_code)
            OTPCode.objects.create(phone_number=form.cleaned_data['phone_number'] , code=random_code)
            request.session['user_registeration_info'] = {
                'phone_number' : form.cleaned_data['phone_number'],
                'email' : form.cleaned_data['email'],
                'full_name' : form.cleaned_data['full_name'],
                'password' : form.cleaned_data['password'],
            }
            messages.success(request , 'we sent you a code ' , 'success')
            return redirect('accounts:verify_code')
        return redirect('home:home')


class UserRegisterVerifyView(View):
    template_name = 'accounts/verify.html'
    form_class = VefiyCodeForm

    def dispatch(self, request, *args, **kwargs): #not in the video
        try:
            user_session = request.session['user_registeration_info']
            OTPCode.objects.get(phone_number=user_session['phone_number'])
        except :
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        form = self.form_class
        return render(request , self.template_name , {'form' : form})

    def post(self , request):
        user_session = request.session['user_registeration_info']
        code_instance = OTPCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_session['phone_number'], email=user_session['email'],
                                         full_name=user_session['full_name'], password=user_session['password'])
                code_instance.delete()
                messages.success(request , 'you are registred successfully ' , 'success')
                return redirect('home:home')
            else:
                messages.error(request , 'code is wrong' , 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
