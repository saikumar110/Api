from django.contrib import admin
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include

app_name="dashboard"

urlpatterns = [
    path('', views.register,name='register'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('account/profile', views.profile,name='profile'),
    path('account/user/patient_profile/user/', views.user_profile,name='user_profile'),
    
    # Account Settings
    path('account/profile/general_settings', views.general_settings,name='general_settings'),
    path('account/profile/password_setting', views.password_setting,name='password_setting'),
    path('account/profile/information_setting', views.information_setting,name='information_setting'),
    path('account/profile/social_setting', views.social_setting,name='social_setting'),
    
    
    # Validations
    path('check/', views.check_username,name='check_username'),
    path('check/', views.check_email,name='check_email'),
    
    #Authentication
    path('auth/login/', views.Login,name='login'),
    path('auth/logout/', views.Logout,name='logout'),
    
     # Password reset urls
    path('password/request-reset-email/', views.RequestPasswordResetEmail,name='request-reset-email'),
    path('password/password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPIView,name='password-reset-confirm'),
    # path('password/password-reset-done/', views.SetNewPasswordAPIView,name='password-reset-complete'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)