from django.urls import path
from . import views
app_name = "dashboard"
urlpatterns = [
    # path('', views.Home , name="home")
    path('home/', views.HomePageView.as_view() , name="home"),
    path('', views.dashboardTemplate , name="dashboartroot")
]
