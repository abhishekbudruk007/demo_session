from django.shortcuts import render ,redirect
from products.models import Product
# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin


@login_required()
def Home(request):
    # context = { "name_list" : ['a','b','h','i','s','h','e','k','b','u','d','u','k']}
    object  = Product.objects.all()
    print ( "object",object)
    context = {'products': object }
    return render(request,'dashboard/home.html',context)


class HomePageView(ListView):
    model = Product
    template_name = 'dashboard/home.html'
    context_object_name = 'products'


def dashboard(request):
    return redirect("dashboard:home")