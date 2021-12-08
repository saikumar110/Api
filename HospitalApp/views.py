from django.shortcuts import render
from .models import Hospital,Doctor,Patient,DiseaseData
from .serializers import HospitalSerializer,PatientDataSerializer,AddPatientSerializer,AddDoctorSerializer,LogoutSerializer,UserSerializer,EmailVerificationSerializer,LoginAPIViewSerializer,EmailSerializer,SetNewPasswordSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .Utils import Utils
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.template.loader import render_to_string,get_template
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.authentication import  TokenAuthentication
from rest_framework import generics
from django.conf import settings
from django.urls import reverse 
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from .permissions import IsHospitalAdmin,IsDoctor
from django.contrib.sites.shortcuts import get_current_site
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

# Views for Registeration 

class RegisterAPIView(generics.GenericAPIView):
   serializer_class =UserSerializer
   permission_classes=[permissions.AllowAny]

#    def get(self, request, format=None):

#              """
#              Return a list of all users.
#              """

#              hospitals = Hospital.objects.all()
#              usernames =  User.objects.all()
#              serializer = HospitalSerializer(hospitals,many=True)
          
#              return Response(serializer.data)

   def post(self, request, format=None):
         
          data= request.data                           # Saving data in data variable and removing hospitalname 
          serializer = self.serializer_class(data=data)
          if serializer.is_valid(raise_exception=True):
                  serializer.create(serializer.validated_data)

                  """-----------Activation Mail Part------------ """

                  user = User.objects.get(email=serializer.validated_data['email'])
                  token = RefreshToken.for_user(user).access_token
                  current_site = get_current_site(request)
                  relativeLink=  reverse('verify-view')
                  absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
               #    email_body="Hi " + user.username +"Use line below to activate your account \n" + absurl
                  email_body =  render_to_string("emails/mail-verify-email.html",locals())
                  data={

                         'domain':absurl,

                         'email_body':email_body,

                         'email_subject':"Verify Your mail",

                         'to_email':user.email,

                    }
                  Utils.send_email(data)
                  print(token) 
                  return Response(serializer.data)
          else:
                    return Response(serializer.errors)


class EmailVerifyAPIView(APIView):

    permission_classes=[permissions.AllowAny]
    serializer_class=EmailVerificationSerializer

    token_param_config =openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])

    
    def get(self,request):
           token = request.GET.get('token')
           try:
               payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
               print(payload['user_id'])
               user = Hospital.objects.get(username_id=payload['user_id'])
            
               if not user.isVerified:
                    user.isVerified = True
                    user.save()
               return Response({"message":"Successfully Activated"})
           except jwt.ExpiredSignatureError:
                return Response({"Error":"ExpiredSignatureError"},status.HTTP_400_BAD_REQUEST)
           except jwt.exceptions.DecodeError :
               return Response({"Error":"DecodeError "})


# Views for the Login 

class LoginAPIView(generics.GenericAPIView):
     permission_classes=[permissions.AllowAny]
     serializer_class=LoginAPIViewSerializer

     
     def post(self, request):
          print(request.data)
          serializer =self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
              

          return Response(serializer.validated_data)


# Views for the Password Reset Via Email

class RequestPasswordResetEmail(generics.GenericAPIView):
     # permission_classes=[IsAuthenticated]
     # authorization_classes=[]
     permission_classes=[permissions.AllowAny]
     serializer_class=EmailSerializer
     # queryset=User

     def post(self,request):
          serializer = self.serializer_class(data=request.data)
          serializer = serializer.is_valid(raise_exception=True)
          """ 
                   The code below send password reset email 
          """
          print(request.data)
          if not request.data or not User.objects.filter(email=request.data['email']).exists():
               return Response("Please valid email address")
          if User.objects.filter(email=request.data['email']).exists():

               user = User.objects.get(email=request.data['email'])

               uidb64 = urlsafe_base64_encode(force_bytes(user.id))

               token = PasswordResetTokenGenerator().make_token(user)
               
               current_site = get_current_site(request)
               relativeLink=  reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
               absurl = 'http://'+str(current_site)+str(relativeLink)
               email_body="Hi " + user.username +"Use line below to activate your account \n" + absurl
               data={

                         'domain':absurl,

                         'email_body':email_body,

                         'email_subject':"Password Reset Link",

                         'to_email':user.email,

               }
               Utils.send_email(data)
               print("done")

          return Response ({"message":"Successfully sent email for password reset"})


class PasswordTokenCheckAPIView(APIView):
     permission_classes = [permissions.AllowAny]
     """ 
             This Class is used for checking token validity and sending the uid and token
     """
     
     def get(self,request,uidb64,token):
     
          try:
               id = smart_str(urlsafe_base64_decode(uidb64))
               user = User.objects.get(id = id)
               
               if not PasswordResetTokenGenerator().check_token(user,token):

                    return Response({
                         "error":"Token is not Valid please request new token"
                    })
               return Response({

                    'Success':True,

                    'message': 'Credentials Valid',

                    'uidb64':uidb64,

                    'token':token
               })

          except DjangoUnicodeDecodeError as identifier:
               return Response({
                         "error":"Token is not Valid please request new token"
                    })     

class SetNewPasswordAPIView(generics.GenericAPIView):
     serializer_class = SetNewPasswordSerializer
     permission_classes = [permissions.AllowAny]
     def patch(self,request):

          serializer = self.serializer_class(data = request.data)

          serializer.is_valid(raise_exception = True)

          return Response({
               'Success':True,
               'Message':'Password reset Successfully ',
          }, status=status.HTTP_200_OK)
          

# Views for Logout 

class LogoutAPIView(generics.GenericAPIView):
     serializer_class = LogoutSerializer
     

     def post(self, request):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          return Response(status=status.HTTP_204_NO_CONTENT)

# Views for Adding doctor 

class AddDoctorAPIView(generics.GenericAPIView):
     serializer_class = AddDoctorSerializer
     permission_classes=[permissions.IsAuthenticated,IsHospitalAdmin]

     def post(self,request):
          serializer = self.serializer_class(data = request.data)
          hospital_object = Hospital.objects.get(username_id=request.user.id)
          # hospital_object="dummyhospital"

          if serializer.is_valid(raise_exception= True):
               serializer.create(serializer.validated_data,hospital_object)
               
               """ -----------Activation Mail Part------------ """
               user =User.objects.get(email=serializer.validated_data['email']) 
               
               doctor = Doctor.objects.get(username_id=user.id)
               token = RefreshToken.for_user(user).access_token   # Creating access token for user

               current_site = get_current_site(request)
               relativeLink=  reverse('verify-doctor')
               absurl = 'http://'+str(current_site)+str(relativeLink)+"?token="+str(token)
               email_body="Hi " + doctor.Full_name +" Use line below to activate your account \n" + absurl

               data={
                         'domain':absurl,
                         'email_body':email_body,
                         'email_subject':"Verify Your mail",
                         'to_email':user.email,
                    }
               Utils.send_email(data)
               return Response(serializer.data)

          else:

               return Response(serializer.errors)
               
# View for Verifying the Doctor's Account

class DoctorAccountEmailVerificationAPIView(APIView):

   
     """

          This View is for verifying the account of Doctor's account   
     
     """
     permission_classes=[permissions.AllowAny]
     def get(self, request):

          token = request.GET.get('token')

          try:
               payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
               print("payload printing")
               # id = payload['user']
               print(payload)
               doctor_obj = Doctor.objects.get(username_id=payload['user_id'])

               if not doctor_obj.isActive :
                    doctor_obj.isActive = True
                    doctor_obj.save()

               return Response({"message":"Sucessfully Activated"})
          except jwt.ExpiredSignatureError:

                return Response({"Error":"ExpiredSignatureError"},status.HTTP_400_BAD_REQUEST)

          except jwt.exceptions.DecodeError :

               return Response({"Error":"DecodeError "})


# Views for the Patient History Access and Patient Addiction Module

class AddPatientAPIView(generics.CreateAPIView):
     serializer_class = AddPatientSerializer
     # permission_classes=[permissions.IsAuthenticated,IsDoctor]
     def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        data=serializer.data

        user,patient = Utils.CreateUserInstance(AccountType='Patient',data=data,request=request)

       # Email for the patient
        email_body="Hi " + patient.Full_name +" your account has been activated on the MEDICAL-DATA-API portal \n"+ 'Username : '+user.username +'\n'+'Email : ' +str(data['email'])+'\n'+'Password : ' +str(data['password']) 

        data={
               'email_body':email_body,
               'email_subject':"Verify Your mail",
               'to_email':user.email,
              }
        Utils.send_email(data)
        return Response({"Message":"Account Created Sucessfully"},status=status.HTTP_204_NO_CONTENT)

""" class RetrieveAPIView(APIView):
     serializer_class = AddPatientSerializer

     # get / retieve patient data
     def get(self, request, *args, **kwargs):
          
           Retieve the patient medical history

          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)

          # Fetch the patient details
          data = Patient.objects.filter(username=User.objects.get(email=serializer.data['email']))
          return Response(self.serializer_class(data,many=True).data)
 """


class PatientHistoryAPIView(generics.GenericAPIView):
     serializer_class =  EmailSerializer
     addSerializer_class = AddPatientSerializer
     EmailSerializer = EmailSerializer
     permission_classes = [permissions.IsAuthenticated,IsDoctor]

     # token_param_config =openapi.Parameter('email',in_=openapi.IN_QUERY,description='Email',type=openapi.TYPE_STRING)
     # @swagger_auto_schema(manual_parameters=[token_param_config])
     
     def get(self,request):
          serializer = self.EmailSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)

          if Utils.IsLastDoctorExamined(request.user, serializer.validated_data['email']):
               try:
                    # serializer = self.EmailSerializer(data = request.data)
                    # serializer.is_valid(raise_exception=True)
                    
                    user_object = get_object_or_404(User,email=serializer.validated_data['email']['email'])         # getting user avaliability
                    patient_object = get_object_or_404(Patient,username=user_object.username) # get patient object
                    patient_history = get_list_or_404(DiseaseData,patient_id=patient_object.id) # getting patient hsitory

                    serializer = self.serializer_class(patient_history,many=True)
                    return Response(serializer.data)
               except :
                    return Response({"email":"Email field required"},status = status.HTTP_400_BAD_REQUEST)
          return Response({"Error " : " You Dont Have Permission to Access the Patient history Get Access "})

     
     def post(self,request):
          serializer = self.addSerializer_class(data = request.data)
          if serializer.is_valid(raise_exception=True):

               serializer.create(serializer.validated_data,request=request)

               return Response(serializer.data,status = status.HTTP_201_CREATED)

class RequestAccessEmail(APIView):

     serializer_class = EmailSerializer
     permission_classes = [permissions.IsAuthenticated,IsDoctor]

     def post(self,request):
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid(raise_exception=True):
               """ 
                    Check if patient Exists or not i.e Validity of email and then send Acess-email
               """
               if not request.data or not User.objects.filter(email=request.data['email']).exists():
                    return Response("Please provide valid email address")

               patient_object = Utils.GetPatientInstance(serializer.validated_data['email']) #Getting the patient Details
               doctor_object = Utils.GetDoctorInstance(request.user)                        # Getting the doctor object


               username = urlsafe_base64_encode(force_bytes(patient_object.username))
               uidb64 = urlsafe_base64_encode(force_bytes(doctor_object.username))
               # token = PasswordResetTokenGenerator().make_token(request.user)
               
               current_site = get_current_site(request)
               relativeLink=  reverse('request-access-confirm',kwargs={'uidb64':uidb64,"username":username})
               absurl = 'http://'+str(current_site)+str(relativeLink)
               email_body="Hi " + patient_object.Full_name +"Use line below to provide access of your mediacl history to the doctor . You can find the details of doctor below \n" + "Doctor Name :" + str(doctor_object.Full_name) + "\n" + "From Hospital : " + str(doctor_object.Hospital_name) +"\n"+absurl
               data={

                         'domain':absurl,

                         'email_body':email_body,

                         'email_subject':"Provide Acess to Doctor FROM MEDICAL-DATA-API",

                         'to_email':serializer.validated_data['email'],

               }
               Utils.send_email(data)
               print("done")

               return Response ({"message":"Successfully sent email for password reset"})

class AccessDataAPIView(APIView):
     permission_classes = [permissions.AllowAny]
     def get(self,request,uidb64,username):
          doctor = smart_str(urlsafe_base64_decode(uidb64))
          username = smart_str(urlsafe_base64_decode(username))
          # print(id)
          # print(username)
          patient_object = Patient.objects.get(username = username)
          patient_object.Last_Doctor_Examined=doctor
          patient_object.save()

          return Response({"message":"Given Access Sucessfully"},status = status.HTTP_200_OK)