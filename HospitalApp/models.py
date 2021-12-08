from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  
# Create your models here.

""" 

     This Module stores the hospitals name , username, password , isActive status and

     step1 : user will post request and send name and username 
     step2 : user will get email with username and password
      
     *imp Hospital user can add doctor and view doctors data



 """
class Hospital(models.Model):
     profile = models.ImageField(upload_to="hospital/",blank=True,null=True)
     username = models.OneToOneField(User,on_delete=models.CASCADE)
     Hospital_name = models.CharField(max_length=30,unique=True)
     bio = models.TextField(blank=True,null=True)
     timings =models.CharField(max_length=300,blank=True,null=True)
     website = models.CharField(max_length=400,blank=True,null=True)
     number = models.CharField(max_length=12,blank=True,null=True)
     Address  = models.CharField(max_length=255,null=True,blank=True)
     twitter = models.CharField(max_length=300,blank=True,null=True)
     facebook = models.CharField(max_length=300,blank=True,null=True)
     google = models.CharField(max_length=300,blank=True,null=True)
     linkedin = models.CharField(max_length=300,blank=True,null=True)
     
     isActive = models.BooleanField(default=False)
     isVerified = models.BooleanField(default=False)
     LastLogin = models.DateTimeField(auto_now_add=True)
     DateJoined = models.DateTimeField(auto_now=True)



"""  This Mdule stores the Doctor name , username, password , isActive status and

     step1 : hospital_admin will post request and send name and username i.e details od doctor 
     step2 : Doctor will get email with username and password
      
     *imp Doctor user can add patient and view patient data """






class Doctor(models.Model):
     profile = models.ImageField(upload_to="doctor/",blank=True,null=True)
     username = models.OneToOneField(User, on_delete=models.CASCADE)
     First_name = models.CharField(max_length=250,blank=True,null=True)
     Last_name = models.CharField(max_length=250,blank=True,null=True)
     # username = models.CharField(max_length=300)

     Hospital_name = models.CharField(max_length=100)
     Experience = models.CharField(max_length=255,blank=True,null=True)
     Address = models.CharField(max_length=255,blank=True,null=True)
     Phone = models.CharField(max_length=12,blank=True,null=True)
     dob = models.DateField(null=True, blank=True)
     email = models.EmailField(null=True, blank=True)
     bio = models.CharField(max_length=255,blank=True,null=True)
     profile = models.ImageField(blank=True,null=True)
     Specializations=models.CharField(max_length=50)
     TotalPatientAttended=models.PositiveIntegerField(default=0)
     isActive=models.BooleanField(default=False)
     

     

"""   This Module stores the Patient name , username, password , isActive status and

     step1 : Doctor will post request and send name and username i.e details od patient 
     step2 : Patient will get email with username and password
      
     *imp Doctor user can add patient and view patient data """




class Patient(models.Model):
     profile = models.ImageField(upload_to="patient/",blank=True,null=True)
     Address = models.CharField(max_length=255,blank=True,null=True)
     Age = models.CharField(max_length=10,blank=True,null=True)
     First_name = models.CharField(max_length=50,blank=True,null=True)
     last_name = models.CharField(max_length=50,blank=True,null=True)
     username = models.CharField(max_length=30,unique = True)
     password = models.CharField(max_length=50)
     created_by = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)
     email = models.EmailField(blank=True,unique=True)
     phone = models.CharField(max_length=10,blank=True,null=True)
     DateJoined = models.DateTimeField(auto_now=True)
     Updated_On =models.DateTimeField(auto_now_add=True, blank=True,null=True)
     LastOtp = models.PositiveIntegerField(default=0)
     OtpActive= models.BooleanField(default=False)
     Last_Doctor_Examined =models.CharField(max_length=50)


class DiseaseData(models.Model):
     patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='patient_data')
     Disease = models.CharField(max_length=100)
     Medicine_Prescribed = models.TextField()
     Doctor = models.CharField(max_length=100)
     Age = models.PositiveIntegerField()
     Hospital_Name = models.CharField(max_length=100)
     weight = models.IntegerField( blank=True)
     isActive = models.BooleanField(default=False)
     DatedON = models.DateTimeField(auto_now=True)
     UpdatedOn = models.DateTimeField(auto_now_add= True)
    