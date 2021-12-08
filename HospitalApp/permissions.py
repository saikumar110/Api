from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User , Group

class IsHospitalAdmin(BasePermission):
     """ 
     
     Allow CRUD object permissions only Hospital Admins
     
     """
     def has_permission(self, request, view):
          # print('permission_classes')
          # print(request.user.id)
          user_obj = User.objects.get(id = request.user.id)
          if user_obj.groups.filter(name = 'hospital_management').exists():
               return True
          return False


class IsDoctor(BasePermission):
     """ 
     
     Allow CRUD object permissions only Hospital Admins
     
     """
     def has_permission(self, request, view):
          # print('permission_classes')
          # print(request.user.id)
          user_obj = User.objects.get(id = request.user.id)
          if user_obj.groups.filter(name = 'Patient Management').exists():
               return True
          return False