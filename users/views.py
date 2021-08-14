from django.shortcuts import render
import base64
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView
from django.views.generic.list import ListView
from .forms import RegistrationForm
from .models import CustomUsers

# Create your views here.
def SignUp(request):
    form = RegistrationForm
    if request.method == "POST":
        registration_form =  RegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid():
            registration_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'User Registered Successfully.')
            return HttpResponseRedirect("/signup")
        else:
            messages.add_message(request, messages.ERROR,
                                 registration_form.errors)
            return HttpResponseRedirect("/signup")
    else:
        context = {"form" : form}
        return render(request,'users/signup.html',context)

def LoginView(request):
    return render(request,"users/login.html")

def decrypt_password(user_encrypt_password):
    """
    Decode base64 encoded string
    :param user_encrypt_password:
    :return: decode base64
    """
    try:
        decoded_password = base64.b64decode(
            user_encrypt_password).decode("utf-8")
    except Exception as error:
        print(error)
        decoded_password = ""
    return decoded_password


def Authenticate(request):
    """Function to check authentication"""
    username_str = request.POST.get('username')
    encrypt_password = request.POST.get('password')

    print(username_str,encrypt_password)

    login_url = '/login/'
    redirect_url = '/home/'
    if username_str and encrypt_password:
        username = username_str
        password = encrypt_password
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            messages.error(request, 'Wrong username/password')
            return HttpResponseRedirect(login_url)
        if user is not None:
            auth_login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, 'Wrong username/password')
            return HttpResponseRedirect(login_url)
    else:
        messages.error(request, 'Please enter username/password')
        return HttpResponseRedirect(login_url)


def LogOut(request):
    """logouts current user and redirect to login page"""
    template_name = 'users/login.html'
    response = HttpResponseRedirect("/login")
    if request.user.is_authenticated:
        try:
            auth_logout(request)
            response.set_cookie('username', value='', max_age=1)
            return response
        except Exception as e:
            print(e)
            pass
    return render(request, template_name)

from django.urls import reverse_lazy
class UpdateUserCBV(UpdateView):
    form_class = RegistrationForm()
    model = CustomUsers
    template_name = 'users/user_update_view.html'
    success_url =   reverse_lazy('dashboard:home')
    # fields = ['username','first_name','last_name','email','user_photo']


from django.contrib.auth.views import PasswordContextMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class PasswordChangeDoneViewCustom(PasswordContextMixin, TemplateView):
    template_name = 'users/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)