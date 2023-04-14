from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Gaming_Deals.sitemaps import *
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# storing all sitemap classes in one dictionary
sitemaps = {
    "staticsitemaps": StaticSitemap,
    "articlessitemap": NewsSitemap,
}


urlpatterns = [
    path('admin/', include('adminpanel.urls')),
    path('accounts/', include('accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/news/', include('news.urls')),
    path('user/', include('userpanel.urls')),
    path('', include('publicarea.urls')),
    path('site.xml',sitemap,{"sitemaps":sitemaps}),
    path('sitemap.xml',TemplateView.as_view(template_name="publicarea/sitemap.xml"),name="SiteMapsMain"),
    path('deals.xml',TemplateView.as_view(template_name="publicarea/deals.xml"),name="SiteMapsDeals"),
    path('robots.txt',TemplateView.as_view(template_name="publicarea/robots.txt"),name="RobotsTxt"),
]

urlpatterns += [
    path('api/', include('news.api_urls')),
    path('api/', include('adminpanel.api_urls')),
]


# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
