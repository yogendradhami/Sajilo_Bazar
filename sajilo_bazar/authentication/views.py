from django.shortcuts import render,redirect
from django.views.generic import  View
from django.contrib.auth.models  import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# from .models import Contact, Blogs

# for activating the user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from  django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError

# email import 
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# getting tokens from utls.py file
from .utils import TokenGenerator,generate_token

# threading
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()



# Create your views here.
def Register(request):
    if request.method == 'POST':
        username= request.POST['username']
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
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

        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.is_active=False
        
        user.save()
        current_site=get_current_site(request)
        email_subject="Activate Your Account."
        message= render_to_string('authentication/activate.html', {
            'user':user,
            'domain':'http://localhost:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
     
        messages.info(request,'Activate Your Account by clicking on your email.')
        return redirect('login')
    
            
    return render(request, 'authentication/register.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user= None

        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,'Account activated successfully.')
            return redirect('login')
        return render(request,'authentication/activatefail.html')



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

def Logout(request):
    logout(request)
    messages.success(request,'Logout Successfully.')
    return redirect('login')