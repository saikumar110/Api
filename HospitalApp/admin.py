from django.contrib import admin
from .models import Hospital,Doctor,Patient,DiseaseData

# Function to get model fields from mode


# Register your models here.
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
     fieldsets = (
        ('BasicDetails', {
            'fields': ('username','Hospital_name','profile')
        }),
        
        ('Permissions', {
            'fields': ( 'isActive','isVerified')
        }),
        
    )
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
     fieldsets = (
        ('BasicDetails', {
            'fields': ('username','First_name','Last_name', 'Hospital_name','Experience','Address','Phone','dob','email','bio','profile','Specializations', 'TotalPatientAttended',)
        }),
        
        ('Permissions', {
            'fields': ( 'isActive',)
        }),
        
            
        
        
    )
     readonly=( 'Last_active',)



admin.site.register(Patient)
admin.site.register(DiseaseData)


from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)