from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = "users"
urlpatterns = [
    path('login/', views.LoginView , name="login"),
    path('logout/', views.LogOut , name="logout"),
    path('signup/', views.SignUp , name="signup"),
    path('user/update/<int:pk>', views.UpdateUserCBV.as_view() , name="update_user_profile"),
    path('authenticate/', views.Authenticate , name="authenticate"),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html',success_url='/logout/') , name="change_password"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             subject_template_name='users/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html'
         ),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),


]
