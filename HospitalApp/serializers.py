from rest_framework import serializers
from .models import Hospital,Doctor,DiseaseData
from django.contrib.auth.models import User
from .Utils import Utils
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50,min_length=6)
    password = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=80,min_length=5)
    hospitalName = serializers.CharField(max_length=80,min_length=2)

    class Meta:
        fields="__all__"

    def validate(self,attrs):
        
        
        if User.objects.filter(email=attrs.get('email')).exists():
            if Utils.checkAvailability(attrs.get('email')):        #Check if user already exist and is not verified so delete 
               # print("TRUE AYA")
               Utils.deleteUnwantedUsers(attrs.get('email'))
            raise serializers.ValidationError("email Already taken ...")

        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError("Username Already taken ...")
        
        if Hospital.objects.filter(Hospital_name=attrs.get('hospitalName')).exists():
            raise serializers.ValidationError("Hospital Account already taken ...")

        return super().validate(attrs)

        
    def create(self, validated_data,hospitalName=None):
        """
        Create and return a new `user` instance, given the validated data in user as well as hospital model.
        """
        try:
             users=User.objects.get(email=validated_data['email'])
             
             if users:
                raise serializers.ValidationError("Email Already Exists")
             """ if hospital:
                raise serializers.ValidationError("Hospital Name Already Exists") """
             
             
        except User.DoesNotExist:
            
            User.objects.create(username=validated_data['username'], password=validated_data['password'],email=validated_data['email'])
            new_user = User.objects.get(username=validated_data['username'])
            new_user.set_password(validated_data['password'])

            hospital_group= Group.objects.get_or_create(name='hospital_management')  # Fetching Hospital Group
            print(hospital_group)
            new_user.groups.add(hospital_group[0].id)
            new_user.is_staff =True
            Hospital.objects.create(username_id=new_user.id,Hospital_name=validated_data['hospitalName'],isActive =True)  # Creating new Hospital instance
            new_user.save()
            return new_user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token']

class LoginAPIViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField() #max_length=255,min_length=6
    password = serializers.CharField() #max_length=68,min_length=6

    class Meta:
        model=User
        fields=['username','password']

    def validate(self,attrs):
      
        username = attrs.get('username',)
        password = attrs.get('password',)

        user = auth.authenticate(username=username, password=password)
        print(user)
        if not user:
            raise AuthenticationFailed(" Invalid Credientials provided ")
        

        try:                                # if token is needed for patient or the doctor then it will pass
            hospital = Hospital.objects.get(username_id=user.id)
            if not hospital.isVerified:
                    raise AuthenticationFailed("Unverified Hospital , Get Verified By email")
        except:
            pass


        token = RefreshToken.for_user(user).access_token

        return {
                'username':user.username,
                'token':str(token),
                'refresh':str(RefreshToken.for_user(user))
        }
       
#  Serializers for Password Reseting

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields=['email']

class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ['username','Hospital_name','isActive']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,max_length=68, write_only=True )
    uidb64 = serializers.CharField(min_length=1, write_only=True )
    token = serializers.CharField(min_length=1, write_only=True )
    
    class Meta:
        fields = ['password','uidb64','token']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            id = force_str(urlsafe_b64decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator.check_token(user,token):
                raise AuthenticationFailed('The reset link is Expired ',401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)
        
        return super().validate(attrs)



class LogoutSerializer(serializers.Serializer):
    refreshtoken = serializers.CharField()

    class Meta:
        fields=['refreshtoken']

    def validate(self,attrs):
        self.token = attrs.get('refreshtoken')

        return attrs

    def save(self,**kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("Bad Token or Invalid Token")


class AddDoctorSerializer(serializers.Serializer):
    full_name = serializers.CharField(min_length=10,max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,max_length=68)
    specialization = serializers.CharField(min_length=6)


    class Meta:
        fields =['full_name','email','password','specialization'] 

    def create(self,validated_data,hospital_object):
       
        try:

            try:

                if Utils.CheckDoctorAvaliablity(validated_data['email']):        #Check if Doctor already exist and is not Active so delete
                        Utils.deleteUnwantedUsers(validated_data['email'])
            except :
                pass
            users=User.objects.get(email=validated_data['email'])

            if users:
                raise serializers.ValidationError("Email Already Exists")

        except User.DoesNotExist:

            # Authentication Credientials addition

            username = Utils.CreateDoctorUsername() # creating a new username
            
            User.objects.create(username=username,email=validated_data['email'])
            user_auth_obj = User.objects.get(email=validated_data['email'])
            user_auth_obj.set_password(validated_data['password'])
            patient_group= Group.objects.get_or_create(name='Patient Management')  # Fetching Hospital Group
            # print(patient_group)

            user_auth_obj.groups.add(patient_group[0].id)
            
            doctor_object = Doctor.objects.create(
                # username = user_auth_obj.id,
                username_id = user_auth_obj.id,
                Hospital_name=hospital_object.Hospital_name,
                Full_name = validated_data['full_name'],
                Specializations=validated_data['specialization']
                 )

            user_auth_obj.save()
       
            print(hospital_object.Hospital_name)
            
            # Doctor Object creation
            
            
            return doctor_object


class AddPatientSerializer(serializers.Serializer):

    First_name =serializers.CharField(min_length=10)
    email = serializers.EmailField(min_length=5)
    password = serializers.CharField(min_length=8)
   
    class Meta:
        fields = '__all__'

    # def create(self, request):

    #     user,patient = Utils.CreateUserInstance(AccountType='Patient',data=request.data,request=request)


    #    # Email for the patient

    #     email_body="Hi " + patient.Full_name +" your account has been activated on the MEDICAL-DATA-API portal \n"+ 'Username : '+user.username +'\n'+'Email : ' +str(data['email'])+'\n'+'Password : ' +str(data['password']) 

    #     data={
    #            'email_body':email_body,
    #            'email_subject':"Verify Your mail",
    #            'to_email':user.email,
    #           }
    #     Utils.send_email(data)
    #     return Response({"Message":"Account Created Sucessfully"},status=status.HTTP_204_NO_CONTENT)


class PatientDataSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = DiseaseData
        fields = "__all__"

class AddPatientSerializer(serializers.ModelSerializer):
    Patientemail = serializers.EmailField() 
    Age = serializers.IntegerField()
    weight = serializers.IntegerField()
    class Meta:
        model = DiseaseData
        fields = ['Patientemail','Disease','Medicine_Prescribed','weight','Age']

    def create(self, validated_data,request):
        """
        Create and return a new `PatientObject` instance, given the validated data.
        """
        doctor_obj = Utils.GetDoctorInstance(request.user)  # Get Doctor info
        patient_object = Utils.GetPatientInstance(validated_data['Patientemail']) #getting patient object
        
        # Updating the Patient attended in doctor object
        doctor_obj.TotalPatientAttended = doctor_obj.TotalPatientAttended+1
        doctor_obj.save()

        data_instance = DiseaseData.objects.create(
            Disease=validated_data['Disease'],
            Medicine_Prescribed=validated_data['Medicine_Prescribed'],
            weight=validated_data['weight'],
            Age=validated_data['Age'],
            Hospital_Name=doctor_obj.Hospital_name,
            Doctor=doctor_obj.Full_name,
            patient_id=patient_object,
        )

        return data_instanceEmailSerializer