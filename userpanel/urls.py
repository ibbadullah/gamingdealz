from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.UserProfileUpdate.as_view(), name='user_panel'),
    path('signup/', views.SingnUpTemplateView.as_view(), name='user_singup'),
    path('login/', views.LoginTemplateView.as_view(), name='user_login'),
    path('logout/', views.logoutUser, name='user_logout'),

    # Setting and customizing default views of Password change and forgot

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password-reset-templates/password_reset_form.html"),
         name="resest_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password-reset-templates/password_reset_done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password-reset-templates/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password-reset-templates/password_reset_complete.html"),
         name="password_reset_complete"),
]
