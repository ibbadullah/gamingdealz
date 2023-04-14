from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test

from . import views

urlpatterns = [
    path('theme/change', views.changeTheme, name='change-theme'),
    path('', user_passes_test(lambda u: u.is_superuser)(TemplateView.as_view(template_name='adminpanel/index.html',
                                                                             extra_context={'page': "Dashboard"})),
         name="home"),
    path('brand/list', views.BrandListView.as_view(), name='brand_list'),
    path('brand/create', views.BrandCreateView.as_view(), name='brand_create'),
    path('brand/edit/<slug>', views.BrandUpdateView.as_view(), name='brand_edit'),
    path('brand/del', views.brandDeletedView, name='brand_del'),
    path('category/list', views.CategoryListView.as_view(), name='category_list'),
    path('category/create', views.CategoryCreateView.as_view(),
         name='category_create'),
    path('category/edit/<slug>',
         views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/del', views.categoryDeletedView, name='category_del'),
    path('product', views.ProductListView.as_view(), name='product_list'),
    path('product/create', views.ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<slug>',
         views.ProductUpdateView.as_view(), name='product_edit'),
    path('product/del', views.productDeletedView, name='product_del'),
    path('searches', views.UserSearchesListView.as_view(), name="search-list"),

    path('favourite/list', views.FavouriteTemplateView.as_view(),
         name="favourite_list"),
    path('offers/list/', views.OfferListView.as_view(), name="offers_list"),
]
