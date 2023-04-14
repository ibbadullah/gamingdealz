from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.PublicareaIndex.as_view(), name='PublicHome'),
    path('all-deals/', views.DealsView.as_view(), name='PublicDeals'),
    path('news/', TemplateView.as_view(template_name="publicarea/news.html"), name='PublicNews'),
    path('favorite-deals/', views.FavoriteDealsView.as_view(),
         name='PublicFavDeals'),
    path('deals/', views.SearchOffer.as_view(), name="PublicProductSearch"),
    path('category-deals/', views.OffersByCategory.as_view(), name="ProductsByCategory"),
    path('news/<slug:slug>', views.NewsDetailView.as_view(), name="PublicNewsDetails"),

    path('about-us', TemplateView.as_view(template_name="publicarea/about-us.html"), name='PublicAboutUs'),
    path('contact-us', TemplateView.as_view(template_name="publicarea/contact-us.html"), name='PublicContactUs'),
    path('datenschutz', TemplateView.as_view(template_name="publicarea/privacy-policy.html"), name='PublicPrivacy'),
]
