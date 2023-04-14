from django.db.models.signals import pre_save
from django.dispatch import receiver
from Gaming_Deals.utitls import unique_slug_generator_product
from adminpanel.models import Brand, Category, Product


@receiver(pre_save, sender=Brand)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)


@receiver(pre_save, sender=Category)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_product(instance)
