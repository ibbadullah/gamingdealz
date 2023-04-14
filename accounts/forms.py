from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import Profile

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=255, label="Full Name")

    class Meta:
        model = User
        fields = {'email', 'name', 'password1', 'password2', 'is_active', 'is_superuser'}


class DelProfileForm(forms.Form):
    current_password = forms.CharField(max_length=255, label="Current password")


class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'first_name', 'last_name', 'img'}


class AccountPasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    new_confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_confirm_password = cleaned_data.get("new_confirm_password")

        if not new_password == new_confirm_password:
            if not len(new_password) > 8:
                raise ValidationError("Password Length not less than 8")
            raise ValidationError("Password Not Mach")
