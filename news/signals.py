from django.db.models.signals import pre_save
from django.dispatch import receiver
from Gaming_Deals.utitls import unique_slug_generator
from news.models import News


@receiver(pre_save, sender=News)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
