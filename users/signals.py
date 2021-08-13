from django.dispatch import receiver
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from .models import UserLogs

@receiver(user_logged_in)
def user_logged_in(sender,request,user,**kwargs):
    print("User is Logged in to the system")
    print("Sender",sender)
    print("request",request)
    print("user",user)

    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=user,
        userlogs_action='user_logged_in',
        userlogs_ip=request.META.get('REMOTE_ADDR')
    )

@receiver(user_logged_out)
def user_logged_out(sender,request,user,**kwargs):
    print("User is Logged in to the system")
    print("Sender",sender)
    print("request",request)
    print("user",user)
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=user,
        userlogs_action='user_logged_out',
        userlogs_ip=request.META.get('REMOTE_ADDR')
    )

