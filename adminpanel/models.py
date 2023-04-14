from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class SearchRecode(models.Model):
    title = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "searchrecode"
        verbose_name = "Search Recode"
        verbose_name_plural = "Search Recode"


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(primary_key=True)
    logo = models.ImageField(upload_to='product/brand/image/', default="product/brand/image/brand.png", null=True,
                             blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "brand"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='product/category/image/', default="product/category/image/category.png",
                              null=True,
                              blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category's"
        db_table = "category"

    def categorycount(self):
        return Product.objects.filter(category__slug=self.slug).count()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(primary_key=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    img = models.ImageField(upload_to='product/image/', default="product/image/product.png", null=True,
                            blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=64)
    clickout_url = models.CharField(max_length=65, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "product"

    def __str__(self):
        return self.name


class Favourite(models.Model):
    offer_id = models.CharField(unique=True, max_length=255)
