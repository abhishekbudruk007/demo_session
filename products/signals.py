from django.dispatch import receiver
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from products.models import Wishlist
from users.models import UserLogs
from django.db.models.signals import post_delete,post_save,pre_save

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





