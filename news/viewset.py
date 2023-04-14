from rest_framework import viewsets
from news.models import News
from news.serializers import NewsListSerializer
from rest_framework import permissions
from django_filters import rest_framework as filters
from .models import GAMING_NEWS


class NewsListAPIView(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['headline', 'category']


class NewsForGamingListAPIView(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]
    queryset = News.objects.filter(category=GAMING_NEWS)
    serializer_class = NewsListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['headline', 'category']
