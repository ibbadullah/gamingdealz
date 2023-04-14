from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import Profile
User = get_user_model()


@receiver(signals.post_save, sender=User)
def make_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()
        Profile(user=instance, first_name="", last_name="").save()
