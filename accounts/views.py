from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.forms import EmailAuthenticationForm, EmailForm, ResetPasswordForm
from django.contrib.auth import get_user_model
from accounts.utils import EmailSender
import random

User = get_user_model()

sender = EmailSender()

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You're already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', True)
            

            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0) 
                
                messages.success(request, f"Welcome back, {user.username}")
                
                return redirect('home')
            
            messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmailAuthenticationForm(request)
     
    context = {
        'form': form,
       
    }
    return render(request, 'auths/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, f"You've been logged out. Goodbye!")
    return redirect('login_view')


def get_user_email(request):
    form = EmailForm()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)

            code = random.randint(0000, 9999)
            user.code=code
            user.save()
            '''sending verification code '''    
            try:
                sender.send_reset_password_code(user)
            except:
                pass 

            messages.success(request, 'a verification code has been sent to your email account, kindly check to reset your password')
            return redirect('reset_password')
        else:
            messages.error(request, 'NO account match with this email')
    else:
        form = EmailForm()

    return render(request, 'auths/email.html', {'form':form})



def reset_password(request):
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():      
            code = form.cleaned_data['code']
            password = form.cleaned_data['new_password']

            user = get_object_or_404(User, code=code)
            user.set_password(password)
            
            user.code = None  
            user.save()
            '''send success message '''   
            try:
                sender.send_reset_password_success_message(user)
            except:
                pass 
            messages.success(request, 'password reset successfully')
            return redirect('login_view')
        else:
            form = ResetPasswordForm()
    else:
        form = ResetPasswordForm()
    
    return render(request, 'auths/reset_password.html', {'form':form})