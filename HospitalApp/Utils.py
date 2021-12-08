from django.core.mail import EmailMessage
from .models import Hospital,Patient,Doctor
from django.contrib.auth.models import User
from datetime import date
import random
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class Utils:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = "html"
        email.send()

    @staticmethod
    def checkAvailability(email1):
        """ 

             This Method return True if user exisit but not verified
             and false if user exist and is verified

         """
        try:
            user = User.objects.get(email=email1)
            print(user.id)
            hopital_obj= Hospital.objects.get(username_id=user.id)
            if hopital_obj and not hopital_obj.isVerified:
                return True
            elif hopital_obj and hopital_obj.isVerified:
                return False
        except Hospital.DoesNotExist:
               return False
        except User.DoesNotExist:
               return False

    @staticmethod
    def deleteUnwantedUsers(email):
         
         """ 
           Delete user who is not Verified
         """
         user = User.objects.get(email=email)
         user.delete()

    @staticmethod
    def OTPgenerator() :
        digits_in_otp = "0123456789"
        OTP = ""
        # for a 4 digit OTP we are using 4 in range
        for i in range(6) : 
            OTP += digits[math.floor(random.random() * 10)] 

        return OTP

    @staticmethod
    def CheckDoctorAvaliablity(email):
        try:
            user = User.objects.get(email=email)
            print('Available email to be deleted 1')
            doc_obj= Doctor.objects.get(user_id=user.id)
            print(doc_obj)
            if doc_obj and not doc_obj.isActive:
                print('Available email to be deleted 2')
                return True
            elif not doc_obj:
                return False
            return False
        except User.DoesNotExist:
            return False
    
    @staticmethod
    def CreateDoctorUsername():
        username = "APIDOC-"+str(date.today()) + "-"+ str(random.choice([i for i in range(0,100)]))  # APIDOC + date + random number
        username = username.replace("-","")
        return username

    @staticmethod
    def CreatePatientUsername():
        username = "APIPAT-"+str(date.today()) + "-"+ str(random.choice([i for i in range(0,100)]))  # APIPAT + date + random number
        username = username.replace("-","")
        return username

    @staticmethod
    def GetDoctorInstance(username):
        user_object = User.objects.get(username = username )
        doctor_object = Doctor.objects.get(username = user_object.id)
        return doctor_object

    @staticmethod
    def GetPatientInstance(email):
        user_object =get_object_or_404( User,email =email )
        patient_object = get_object_or_404(Patient,username = user_object.username)
        return patient_object

    @classmethod
    def CreateUserInstance(self,AccountType,data,request):
        # print(self.CreatePatientUsername())
        if AccountType=="Patient":
            
            # check if user already exists
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Patient Already Exists")
            
            # Creating the Authentication object
            user=User.objects.create(username=self.CreatePatientUsername(),password=data['password'],email=data['email'])
            user.set_password(data['password'])
            user.save()
            
            #Creating Patient details objects
            print(request.user.username)
            patient=Patient.objects.create(username=user.username,
                                            Full_name=data['full_name'],
                                            created_by_id=(Hospital.objects.get(username_id=request.user.id)).id,
                                            Last_Doctor_Examined=request.user.username)
            return user,patient

    @classmethod
    def IsLastDoctorExamined(self,username,patientemail):
            patient_object = self.GetPatientInstance(patientemail)
            # print(str(username) == str(patient_object.Last_Doctor_Examined))
            # print(username)
            # print(patient_object.Last_Doctor_Examined)
            if str(username) == str(patient_object.Last_Doctor_Examined):
                print("True")
                return True
            else : 
                return False