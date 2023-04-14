from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import (SearchRecode, Brand, Product, Category, Favourite)
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from django.conf import settings
from django.urls import reverse_lazy


@login_required
def changeTheme(request):
    try:
        if request.session['theme'] in 'light':
            request.session['theme'] = 'dark'
        else:
            request.session['theme'] = 'light'
    except Exception as e:
        pass
    if request.GET.get('path'):
        return HttpResponseRedirect(request.GET.get('path'))
    return HttpResponseRedirect('/')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BrandListView(ListView):
    paginate_by = 20
    model = Brand
    extra_context = {'page': "Products"}

    def get_queryset(self):
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')
        status = self.request.GET.get('status')
        brand = self.model.objects.all()
        if search:
            brand = brand.filter(name__icontains=search)
        if sort == "desc":
            brand = brand.order_by('-id')
        if status == "active":
            brand = brand.filter(active=True)
        if status == "deactivate":
            brand = brand.filter(active=False)
        return brand


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BrandCreateView(SuccessMessageMixin, CreateView):
    model = Brand
    fields = ['name', 'logo', 'active']
    success_url = reverse_lazy('brand_list')
    success_message = "%(name) has created successfully"
    extra_context = {'page': "Products"}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BrandUpdateView(SuccessMessageMixin, UpdateView):
    model = Brand
    fields = ['name', 'logo', 'active']
    success_url = reverse_lazy('brand_list')
    success_message = "%(name) has updated successfully"
    extra_context = {'page': "Products"}


@login_required
def brandDeletedView(request):
    if request.method == "POST":
        try:
            id = request.POST.get("input_del")
            print(id)
            if id:
                print(id)
                user = get_object_or_404(Brand, pk=id)
                name = user.name
                user.delete()
                messages.success(request, f'This {name} Brand Deleted...!')
                return redirect('brand_list')
        except Exception as e:
            messages.error(request, 'Error on Deleted Brand')
            return redirect('brand_list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryListView(ListView):
    model = Category
    paginate_by = 20
    extra_context = {'page': "Products"}

    def get_queryset(self):
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')
        status = self.request.GET.get('status')
        by = self.request.GET.get('by')
        category = self.model.objects.all()
        if by == "name":
            category = category.filter(name__icontains=search)
        if by == "description":
            category = category.filter(description__icontains=search)
        if sort == "desc":
            category = category.order_by('-id')
        if status == "active":
            category = category.filter(active=True)
        if status == "deactivate":
            category = category.filter(active=False)
        return category


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name', 'description', 'image', 'active']
    success_url = reverse_lazy('category_list')
    extra_context = {'page': "Products"}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'image', 'active']
    success_url = reverse_lazy('category_list')
    success_message = "%(name) has Updated successfully"
    extra_context = {'page': "Products"}


@login_required
def categoryDeletedView(request):
    if request.method == "POST":
        try:
            id = request.POST.get("input_del")
            print(id)
            if id:
                category = get_object_or_404(Category, pk=id)
                name = category.name
                category.delete()
                messages.success(request, f'{name} Category has Deleted...!')
                return redirect('category_list')
        except Exception as e:
            print(e)
            messages.error(request, 'Error on Deleted Category')
            return redirect('category_list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductListView(ListView):
    model = Product
    extra_context = {'page': "Products"}

    def get_queryset(self):
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')
        status = self.request.GET.get('status')
        by = self.request.GET.get('by')
        product = self.model.objects.all()
        if by == "name":
            product = product.filter(name__icontains=search)
        if by == "description":
            product = product.filter(description__icontains=search)
        if by == "brand":
            product = product.filter(brand__name__icontains=search)
        if by == "category":
            product = product.filter(category__name__icontains=search)
        if sort == "desc":
            product = product.order_by('-id')
        if status == "active":
            product = product.filter(active=True)
        if status == "deactivate":
            product = product.filter(active=False)
        return product


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    fields = ['name', 'img', 'brand', 'category',
              'description', 'price', 'clickout_url', 'active']
    success_url = reverse_lazy('product_list')
    success_message = "%(name) has Updated successfully"
    extra_context = {'page': "Products"}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    fields = ['name', 'img', 'brand', 'category',
              'description', 'price', 'clickout_url', 'active']
    success_url = reverse_lazy('product_list')
    success_message = "%(name) has Updated successfully"
    extra_context = {'page': "Products"}


@login_required
def productDeletedView(request):
    if request.method == "POST":
        try:
            id = request.POST.get("input_del")
            print(id)
            if id:
                product = get_object_or_404(Product, pk=id)
                name = product.name
                product.delete()
                messages.success(request, f'{name} Category has Deleted...!')
                return redirect('product_list')
        except Exception as e:
            messages.error(request, 'Error on Deleted Category')
            return redirect('product_list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserSearchesListView(ListView):
    paginate_by = 20
    ordering = ['-id']
    model = SearchRecode
    extra_context = {'page': "Searches"}


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class FavouriteTemplateView(TemplateView):
    template_name = 'adminpanel/favourite_list.html'
    extra_context = {'page': 'Our Favorites'}

    def get(self, request, *args, **kwargs):
        ids_list = ''
        for i in Favourite.objects.all():
            ids_list += i.offer_id + ','
        ids_list = ids_list[:-1:]
        response = requests.get(f"{settings.OFFER_API}offers/{ids_list}",
                                auth=(settings.OFFER_USERNAME, settings.OFFER_PASSWORD))
        response = response.json()
        self.extra_context['data'] = response
        return render(request, self.template_name, self.extra_context)

    def post(self, request, *args, **kwargs):
        d = Favourite.objects.get(offer_id=request.POST.get('Remove'))
        id = d.offer_id
        d.delete()
        messages.success(request, f"Favourite {id} is Remove")
        return redirect('favourite_list')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OfferListView(TemplateView):
    template_name = 'adminpanel/offers_list.html'
    extra_context = {'page': 'API Products'}
    model = Favourite

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        offset = request.GET.get('offset')
        newPart = "&document_types=offer&document_types=product_offer"
        if not offset:
            offset = 0
        else:
            offset = int(offset)
        if search:
            response = requests.get(f"{settings.OFFER_API}search-results?q={search}&offset={offset}{newPart}",
                                    auth=(settings.OFFER_USERNAME, settings.OFFER_PASSWORD))
            response = response.json()
            self.extra_context['data'] = response
        return render(request, self.template_name, self.extra_context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('Favourite'):
            d = Favourite(offer_id=request.POST.get('Favourite'))
            d.save()
            messages.success(request, f"Favourite Added..!")
        else:
            d = Favourite.objects.get(offer_id=request.POST.get('Remove'))
            id = d.offer_id
            d.delete()
            messages.success(request, f"Favourite {id} is Remove")
        return redirect('offers_list')
