from django.urls import path,include
from . import viewset as views
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('news', views.NewsListAPIView,basename='news')
route.register('gamingnews', views.NewsForGamingListAPIView,basename='gamingnews')


urlpatterns = [
    path('news/', include(route.urls))
]
