from django.contrib.sitemaps import Sitemap
from news.models import *
from django.shortcuts import reverse

# Sitemap class for static views/pages
class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    # builtin view for defining static views names
    def items(self):
        return ['PublicHome',"PublicDeals","PublicNews","PublicAboutUs","PublicContactUs","PublicPrivacy"]

    # builtin view for reversing
    def location(self, item):
        return reverse(item)


# Sitemap for services model
class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return News.objects.all()