from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from accounts.forms import UserCreateForm, DelProfileForm, UserUpdateProfileForm, AccountPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from accounts.models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
User = get_user_model()


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserListView(ListView):
    template_name = 'accounts/user_list.html'
    model = User
    paginate_by = 30
    ordering = ['id']
    extra_context = {'page': "Users"}

    def get_queryset(self):
        search = self.request.GET.get('search')
        by = self.request.GET.get('by')
        role = self.request.GET.get('role')
        status = self.request.GET.get('status')
        sort = self.request.GET.get('sort')
        user = User.objects.all()
        if by == "name": user = user.filter(name__icontains=search)
        if by == "email": user = user.filter(email__icontains=search)
        if role == "1": user = user.filter(is_superuser=True)
        if role == "0": user = user.filter(is_superuser=False)
        if sort == "desc": user = user.order_by('-id')
        if status == "active": user = user.filter(is_active=True)
        if status == "deactivate": user = user.filter(is_active=False)
        return user


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('users-list')
    form_class = UserCreateForm
    success_message = "%(name)s has created successfully"
    extra_context = {'page': "Users"}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('users-list')
    fields = ["name", "email", "is_active", "is_superuser"]
    success_message = "%(name)s has updated successfully"
    model = User
    extra_context = {'page': "Users"}


@login_required
def userDeleteView(request):
    if request.method == "POST":
        try:
            id = request.POST.get("input_del")
            if id:
                user = get_object_or_404(User, pk=id)
                email = user.email
                user.delete()
                messages.success(request, f'This {email} User Deleted...!')
                return redirect('users-list')
        except Exception as e:
            messages.error(request, 'Error on Deleted User')
            return redirect('users-list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserAccounts(TemplateView):
    template_name = "accounts/account.html"


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserProfileDel(TemplateView):
    template_name = "accounts/profileDel.html"
    extra_context = {'form': DelProfileForm()}

    def post(self, request, *args, **kwargs):
        form = DelProfileForm(request.POST)
        password = None
        if form.is_valid():
            password = form.cleaned_data['current_password']
        else:
            messages.error(request, "Wrong")
        user = User.objects.get(email=request.user.email)
        if user.check_password(password):
            user.delete()
            messages.success(request, "User has Deleted Successfully..!")
        else:
            messages.error(request, "Wrong Password")
        return redirect('user-profile-del')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserProfileUpdate(TemplateView):
    template_name = 'accounts/profile_form.html'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, pk=self.request.user.profile.id)
        form = UserUpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has Updated..!")
        else:
            messages.error(request, "Profile has Not Updated..!")
        return redirect('user-profile-edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(Profile, pk=self.request.user.profile.id)
        context['form'] = UserUpdateProfileForm(instance=user)
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserAccountPasswordChange(TemplateView):
    template_name = "accounts/accountpasschange.html"
    extra_context = {'form': AccountPasswordChangeForm()}

    def post(self, request, *args, **kwargs):
        theme = request.session.get('theme')
        form = AccountPasswordChangeForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=self.request.user.id)
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has Changed.")
                request.session['theme'] = theme
                return redirect('account-password-change')
            messages.error(request, "Old password was wrong.")
        return render(request, self.template_name, {'form': form})




to = "parker.student0315@gmail.com"
title = "Testing"
message = "This is a testing message."
template_location = "templates/base.html"

# Email sender
def EmailSender(request,to = "parker.student0315@gmail.com",title = "Testing",message = "This is a testing message.",
                template_location= "email.html"):

    html_content = render_to_string(template_location,{"Title": title, "Message": message})

    text_content = strip_tags(html_content)

    sendEmail = EmailMultiAlternatives(
        # Title of the message
        title,
        # Message body
        text_content,
        # From Email
        settings.EMAIL_HOST_USER,
        # To email
        [to]
    )

    sendEmail.attach_alternative(html_content, "text/html")
    sendEmail.send()