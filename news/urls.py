from django.urls import path
from news import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('create', views.NewsCreateView.as_view(), name='news_create'),
    path('edit/<slug>', views.NewsUpdateView.as_view(), name='news_edit'),
    path('del', views.newDeleteView, name='news_del'),
]