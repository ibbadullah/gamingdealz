from rest_framework import serializers
from adminpanel.models import SearchRecode, Product, Category, Brand


class SearchRecodeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchRecode
        fields = ['title', 'ip']


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductBrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'slug']


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = ProductCategoryModelSerializer(instance.category).data
        response['brand'] = ProductBrandModelSerializer(instance.brand).data
        return response

