from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager


class User(AbstractUser):
    username = first_name = last_name = None
    name = models.CharField(max_length=255)
    objects = UserManager()
    is_staff = models.BooleanField(default=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'user'
        verbose_name = _(" User")
        verbose_name_plural = _(" Users")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    img = models.ImageField(upload_to='accounts/profile/', default='accounts/profile/profile.png')

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = "profile"
        verbose_name = _(' Profile')
        verbose_name_plural = _(" Profile")

    @property
    def profile_img(self):
        return self.img

    @property
    def full_name(self):
        if not self.first_name or self.last_name:
            return "unknown"
        return f"{self.first_name} {self.last_name}"

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_last_login(self):
        return self.user.last_login

    @property
    def user_join(self):
        return self.user.date_joined


class LastLogin(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = "lastlogin"
        verbose_name = _('Last Login')
        verbose_name_plural = _("Last Login")
