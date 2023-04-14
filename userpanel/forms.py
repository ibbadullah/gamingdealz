from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import Profile
User = get_user_model()
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=300,)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'img']
