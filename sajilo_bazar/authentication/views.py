from django.shortcuts import render,redirect
from django.contrib.auth.models  import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# from .models import Contact, Blogs
# email import 
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.
def Register(request):
    if request.method == 'POST':
        username= request.POST['username']
        first_name= request.POST['fname']
        last_name= request.POST['lname']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is not matching.")
            return  redirect('register')
        
        try:
            if User.objects.get(username=username):
                messages.warning(request,'Username is already taken.')
                return redirect('register')
        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request,'Email is already taken.')
                return redirect('register')
        except Exception as identifier:
            pass

        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=first_name
        myuser.last_name=last_name
        myuser.save()
        messages.info(request,'Signup successful.  Please Login.')
        return redirect('login')
    
            
    return render(request, 'authentication/register.html')

def Login(request):
    if request.method == 'POST':
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successfully.")
            return render(request, 'base.html')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect('login')

    return render(request, 'authentication/login.html')