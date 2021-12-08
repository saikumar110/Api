from django.urls import path
from.views import RegisterAPIView,AddPatientAPIView,AccessDataAPIView,RequestAccessEmail,PatientHistoryAPIView,AddDoctorAPIView,DoctorAccountEmailVerificationAPIView,EmailVerifyAPIView,LoginAPIView,RequestPasswordResetEmail,PasswordTokenCheckAPIView,SetNewPasswordAPIView,LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # Registertaion urls
    path('register/', RegisterAPIView.as_view(),name='registerView'),
    path('register/verify-view/', EmailVerifyAPIView.as_view(),name='verify-view'),


    # Password reset urls
    path('password/request-reset-email/', RequestPasswordResetEmail.as_view(),name='request-reset-email'),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPIView.as_view(),name='password-reset-confirm'),
    path('password/password-reset-done/', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),

    # Add Doctor Urls
    path('doctor/add-doctor/', AddDoctorAPIView.as_view(),name='add-doctor'),
    path('doctor/verify-doctor-account/', DoctorAccountEmailVerificationAPIView.as_view(),name='verify-doctor'),

    # Add Patient urls
    # path('add-patient/', RetrieveAPIView.as_view(),name='add-patient'),
    path('patient/history/', PatientHistoryAPIView.as_view(),name='add-patient'),

    # Patient Access urls
    path('access/request-acess-email/', RequestAccessEmail.as_view(),name='request-acess-email'),
    path('access/request-access/<uidb64>/<username>', AccessDataAPIView.as_view(),name='request-access-confirm'),
   

    # Login urls
    path('login/', LoginAPIView.as_view(),name='login-view'),

    # Logout urls
    path('logout/',LogoutAPIView.as_view(),name="logout"),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   
]
