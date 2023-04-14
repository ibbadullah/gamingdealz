from rest_framework import serializers
from news.models import News
from django.contrib.auth import get_user_model

User = get_user_model()


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
