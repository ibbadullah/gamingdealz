from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from .forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.views import LoginView
from accounts.models import Profile, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class SingnUpTemplateView(TemplateView):
    template_name = 'userpanel/signup.html'

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url=reverse_lazy('user_login')), name='dispatch')
class UserProfileUpdate(TemplateView):
    template_name = "userpanel/user_profile.html"

    def get(self, request, *args, **kwargs):
        id = request.user.profile.id
        instance = get_object_or_404(Profile, pk=id)
        form = UserProfileForm(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id = request.user.profile.id
        instance = get_object_or_404(Profile, pk=id)
        form = UserProfileForm(request.POST or None,request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            user = User.objects.get(pk=request.user.pk)
            user.email = email
            user.save()
        return render(request, self.template_name, {'form': form})


class LoginTemplateView(LoginView):
    template_name = 'userpanel/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_panel')
        messages.error(request, 'Wrong Information')
        return render(request, self.template_name)


@login_required(login_url=reverse_lazy('user_login'))
def logoutUser(request):
    logout(request)
    return redirect('user_login')


