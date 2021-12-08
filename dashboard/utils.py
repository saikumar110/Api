from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from twilio.rest import Client
# Validations
def check_username(name):

     # Fetch the object
     try:
          obj = get_object_or_404(User,username=name)
          return True
     except :
          return False
          

def check_email(request):
     # Fetch the object
     try:
          obj = get_object_or_404(User,email=data.get('email'))
          return True
     except :
          return False
def send_sms():
     account_sid = 'AC1f570ea9674ee724789f032c9bc0477d'
     auth_token = '895795fdeed3c4d76d37ddd208d8621b'
     client = Client(account_sid, auth_token)
     try:
          message = client.messages.create(
                                        body="Hey Bala how's chinmayee",
                                        from_='+17035968135',
                                        to='+919967491709'
                    )
          return True
     except:
          return False
