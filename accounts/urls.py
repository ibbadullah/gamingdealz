from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.UserListView.as_view(), name='users-list'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create', views.UserCreateView.as_view(), name='users-create'),
    path('edit/<int:pk>', views.UserUpdateView.as_view(), name='users-edit'),
    path('del/', views.userDeleteView, name='users-del'),
    path('profile', views.UserAccounts.as_view(), name='user-account'),
    path('profile/edit', views.UserProfileUpdate.as_view(), name='user-profile-edit'),
    path('profile/del', views.UserProfileDel.as_view(), name='user-profile-del'),
    path("account/password/change", views.UserAccountPasswordChange.as_view(), name="account-password-change"),

]
