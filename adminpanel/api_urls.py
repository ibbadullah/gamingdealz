from django.urls import path, include
from . import viewset as views
from rest_framework.routers import DefaultRouter

route = DefaultRouter()

route.register('category', views.CategoryModelViewSet)
route.register('brands', views.BrandModelViewSet)
route.register('products', views.ProductModelViewSet)

urlpatterns = [
    path('search', views.SearchRecodeCreateAPIView.as_view()),
    path('product/', include(route.urls)),
    path('getsearch', views.getSearchRecommand),
    # start endpoints
    path('offerIds', views.OfferIdsAPI),
    path('search-results', views.searchAPI),
    path('search/category-results', views.searchCategortAPI),
    path('categories/roots', views.categoriesRoots),
    path('categories/tree', views.categoriesTree),
    path('categories/<str:id>', views.Categories),
    path('offers/<str:id>', views.getOffers),
]
