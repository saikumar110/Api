from django.shortcuts import render,redirect 
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponseRedirect
from .utils import*
import socket
from twilio.rest import Client
from django.utils.encoding import force_bytes, force_str
import base64
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from HospitalApp.Utils import Utils
from django.template.loader import render_to_string
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from HospitalApp.models import Hospital
from django.contrib.auth.models import Group

# Default Registeration Page
def register(request,template_name="dashboard/register.html"):
     if request.method == "POST":
          name = request.POST.get("register-username")
          email = request.POST.get("register-email")
          password = request.POST.get("register-password")
          
          # validation for email and username
          if User.objects.filter(email=email).exists():
               if Utils.checkAvailability(email):        #Check if user already exist and is not verified so delete 
                    Utils.deleteUnwantedUsers(email)
                    
               messages.add_message(request, messages.ERROR, 'Email Already taken ...',fail_silently=True)
               return render(request, template_name,locals())
               
          if User.objects.filter(username=name).exists():#Check if user already exist  
               messages.add_message(request, messages.ERROR, 'Username Already taken ...',fail_silently=True)
               return render(request, template_name,locals())
          # print("--------------------------")
          
          # Creating The New user Instance
          User.objects.create(username=name, password=password,email=email)
          new_user = User.objects.get(username=name)
          # new_user.
          new_user.set_password(password)

          hospital_group= Group.objects.get_or_create(name='hospital_management')  # Fetching Hospital Group
          print(hospital_group)
          new_user.groups.add(hospital_group[0].id)
          new_user.is_staff =True
          
          # Creating Hospital instance
          Hospital.objects.create(username_id=new_user.id,Hospital_name=name,isActive =True,profile = request.FILES['profile'])  # Creating new Hospital instance
          new_user.save()
          
          """-----------Activation Mail Part------------ """
          
          user = User.objects.get(email=email)
          token = RefreshToken.for_user(user).access_token
          current_site = get_current_site(request)
          relativeLink=  reverse('verify-view')
          absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
          #    email_body="Hi " + user.username +"Use line below to activate your account \n" + absurl
          email_body =  render_to_string("emails/mail-verify-email.html",locals())
          data={

               'domain':absurl,

               'email_body':email_body,

               'email_subject':"MedBoto Account Activation",

               'to_email':user.email,
          }
          Utils.send_email(data)
         
          
            
          messages.add_message(request, messages.SUCCESS, 'test',fail_silently=False)
          return render(request, template_name,locals())
     return render(request, template_name)

# Account Settings

#  1) General
def general_settings(request,template_name="dashboard/profile.html"):
     
     user = get_object_or_404(User, pk=request.user.pk)
     
     if request.method =='POST':
          print(request.POST)
          first_name = request.POST.get('first_name',None)
          last_name = request.POST.get('last_name',None)
          email = request.POST.get('email',None)
          hospital = request.POST.get('hospital',None)
          
          user_obj = get_object_or_404(User, pk=request.user.pk)
          user_obj.first_name = first_name
          user_obj.last_name = last_name
          user_obj.email = email
          user_obj.username = hospital
          user_obj.save()
          
          # Add success message
          messages.add_message(request, messages.SUCCESS,"Updated successfully",fail_silently=True)
          return redirect('dashboard:profile')
     return render(request, template_name,locals())

#  2) Change password
def password_setting(request,template_name="dashboard/profile.html"):
     if request.method =="POST":
          password1 = request.POST.get('new-password')
          password2 = request.POST.get('confirm-new-password')
          print(request.user)
          if password1 == password2:
               user_obj = get_object_or_404(User, pk=request.user.pk)
               user_obj.set_password(password1)
               user_obj.save()
               messages.add_message(request, messages.SUCCESS,"Updated successfully",fail_silently=True)
               return redirect('dashboard:profile')
     messages.add_message(request, messages.ERROR, 'Password dosent match ',fail_silently=True)
     return render(request,"dashboard/profile.html",locals()) 

#  3) Information
def information_setting(request):
     if request.method =="POST" :
          print(request.POST)
          bio = request.POST.get('bio')
          timings = request.POST.get('timing')
          address = request.POST.get('Address')
          website = request.POST.get('website')
          phone = request.POST.get('phone')
          
          hospital = Hospital.objects.get(username=request.user)
          hospital.bio = bio
          hospital.Address = address
          hospital.number = phone
          hospital.website = website
          hospital.timings = timings
          hospital.save()
     return redirect('dashboard:profile')

# 4) Social
def social_setting(request):
     if request.method =="POST":
          hosp_obj = get_object_or_404(Hospital, username=request.user)
          if hosp_obj is not None:
               hosp_obj.twitter = request.POST.get('twitter')
               hosp_obj.facebook = request.POST.get('facebook')
               hosp_obj.google = request.POST.get('google')
               hosp_obj.linkedin    = request.POST.get('linkedin')
               hosp_obj.save()
     return redirect('dashboard:profile')

@login_required(login_url='dashboard:login')
def dashboard(request,template_name="dashboard/dashboard.html"):
     # Data for locals()
     try:
          user = Hospital.objects.get(username=request.user)
     except:
          pass
     if user:
          return render(request, template_name,locals())
     return render(request,"authentication/404.html")



# Authentications Views
@login_required(login_url='dashboard:login')
def profile(request,template_name="dashboard/profile.html"):
     # Data for locals()
     print(request.user)
     hospital = Hospital.objects.get(username=request.user)
     user = User.objects.get(username=request.user)
     print(user)
     return render(request, template_name,locals())

def user_profile(request,template_name="dashboard/default_dashboard.html"):
     return render(request, template_name)

def Login(request,template_name="authentication/login.html"):
     if request.method =='POST':
          
          # Fetching The User Details from Client Side
          email = request.POST['login-email']
          password = request.POST['login-password']
          # Fetching the user Details from User Model
          try:
               
               user = User.objects.get(email=email)
               user = authenticate(request, username=user.username, password=password)
               if user is not None:
                    login(request, user)
                    print("loign")
                    # Redirect to a success page.
                    return redirect('dashboard:dashboard')
                    
               else:
                    messages.add_message(request,messages.ERROR,"s",fail_silently=True)
                    return render(request, template_name,locals())
          except:
               messages.add_message(request,messages.ERROR,"s",fail_silently=True)
               return render(request, template_name,locals())
     return render(request, template_name)
      
def Logout(request):
     logout(request)
     return redirect('dashboard:login') 

def RequestPasswordResetEmail(request,template_name="authentication/forgot-password.html"):
     if request.method =='POST': 
          print(request.POST)
          if User.objects.filter(email=request.POST.get('forgot-password-email')).exists():

               user = User.objects.get(email=request.POST.get('forgot-password-email'))

               uidb64 = urlsafe_base64_encode(force_bytes(user.id))

               token = PasswordResetTokenGenerator().make_token(user)
               
               hostname = socket.gethostname()
               ip_address = socket.gethostbyname(hostname)
                    
               current_site = get_current_site(request)
               relativeLink=  reverse('dashboard:password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
               absurl = 'http://'+str(current_site)+str(relativeLink)
               # email_body="Hi " + user.username +"Use line below to activate your account \n" + absurl
               email_body = render_to_string("authentication/mail-reset-password.html",locals())
               data={

                    'domain':absurl,

                    'email_body':email_body,

                    'email_subject':"Password Reset Link",

                    'to_email':user.email,
               }
               Utils.send_email(data)
               print("done")
               messages.add_message(request, messages.SUCCESS, "Password reset mail sent",fail_silently=True)
               return render(request,template_name,locals())
          else:
               messages.add_message(request, messages.ERROR, "Invalid Email Address",fail_silently=True)
               return render(request,template_name,locals())
     return render(request, template_name,locals())      

def PasswordTokenCheckAPIView(request, uidb64,token,template_name="authentication/password-reset.html"):
     
     if request.method=="POST" :
          print(request.POST)
          print("------dshdajds--------------")
          id = smart_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(id=id)
          p = PasswordResetTokenGenerator()
          print(p.check_token(user,token))
          if not p.check_token(user,token):
               print("Expired")
          user.set_password(request.POST.get("reset-password-confirm"))
          user.save()
          return render(request, "authentication/login.html")
     return render(request, template_name, locals())

def SetNewPasswordAPIView(request,template_name="authentication/login.html"):
     if request.method=="POST" :
          print("------dshdajds--------------")
     return render(request, template_name, locals)
