from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()

NEWS = 'News'
GAMING_NEWS = "Gaming News"


class News(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    img = models.ImageField(upload_to='news/images/cover/')
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True, choices=(
        (NEWS, NEWS), (GAMING_NEWS, GAMING_NEWS)))
    headline = models.CharField(max_length=500)
    dec = models.TextField(null=True, blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    text = RichTextUploadingField(config_name="ck2", null=True, blank=True)
    button_text1 = models.CharField(max_length=255, null=True, blank=True)
    link_url1 = models.URLField(max_length=1000, null=True, blank=True)
    offer_Button = models.CharField(max_length=255, null=True, blank=True)
    offer = models.CharField(max_length=250, null=True, blank=True)
    activate = models.BooleanField(default=True)
    create_on = models.DateField(auto_now_add=True)
    text2 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'news'
        verbose_name = _('News')
        verbose_name_plural = _("News")

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return f"/news/{self.slug}"
