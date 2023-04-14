from rest_framework import generics, response, viewsets, permissions
from adminpanel.models import SearchRecode, Category, Product, Brand, Favourite
from adminpanel.serializers import SearchRecodeModelSerializer, CategoryModelSerializer, BrandModelSerializer, \
    ProductModelSerializer
from django_filters import rest_framework as filters
from .pagination import LargeResultsSetPagination
from django.http import JsonResponse
import requests
from Gaming_Deals.settings import OFFER_USERNAME, OFFER_PASSWORD, OFFER_API


def getSearchRecommand(request):
    d = SearchRecode.objects.order_by('-id').filter(ip=request.user_ip).first()
    return JsonResponse({'search': d.title})


class SearchRecodeCreateAPIView(generics.CreateAPIView):
    queryset = SearchRecode.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchRecodeModelSerializer

    def create(self, request, *args, **kwargs):
        try:
            SearchRecode(title=request.data.get(
                'title'), ip=request.user_ip).save()
        except Exception as e:
            return response.Response({'error': 'Error on Search Recode Created'})
        return response.Response({'success': 'Search Recode Created successfully'})


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(active=True)
    serializer_class = CategoryModelSerializer
    http_method_names = ['get']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['name']


class BrandModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Brand.objects.filter(active=True)
    serializer_class = BrandModelSerializer
    http_method_names = ['get']


class ProductModelViewSet(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['name', 'category', 'brand']

    def get_queryset(self):
        recommend = self.request.GET.get('recommend')
        sort = self.request.GET.get('sort')
        price_amount_lte = self.request.GET.get('price_amount_lte')
        price_amount_gte = self.request.GET.get('price_amount_gte')
        dprice = self.request.GET.get('price')
        brand = self.request.GET.get('brand')
        categorie = self.request.GET.get('categorie')
        q = self.request.GET.get('q')
        products = self.queryset
        if sort:
            products = products.order_by(sort)
        if dprice:
            products = products.order_by(dprice)
        if recommend:
            products = products.filter(name__icontains=recommend)
        if q:
            products = products.filter(name__icontains=q)
        if brand:
            products = products.filter(brand__slug=brand)
        if price_amount_gte:
            products = products.filter(price__gte=price_amount_gte)
        if price_amount_lte:
            products = products.filter(price__lte=price_amount_lte)
        if categorie:
            products = products.filter(category__slug=categorie)
        return products


def OfferIdsAPI(request):
    ids_list = ''
    for i in Favourite.objects.all():
        ids_list += i.offer_id + ','
    res = requests.get(f'{OFFER_API}offers/{ids_list[:-1:]}', auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    if res.get('status') == 404:
        res = {'items': []}
    return JsonResponse(res)


def searchAPI(request):
    query = '&'
    if request.GET.get('q'):
        query = query + f"q={request.GET.get('q')}"
    if request.GET.get('offset'):
        query = query + f"&offset={request.GET.get('offset')}"
    if request.GET.get('sort'):
        query = query + f"&sort={request.GET.get('sort')}"
    if request.GET.get('filters[price_amount_lte]'):
        query = query + f"&filters[price_amount_lte]={request.GET.get('filters[price_amount_lte]')}"
    if request.GET.get('filters[price_amount_gte]'):
        query = query + f"&filters[price_amount_gte]={request.GET.get('filters[price_amount_gte]')}"
    res = requests.get(f"{OFFER_API}search-results?{query}", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)


def searchCategortAPI(request):
    query = '&'
    if request.GET.get('filters[categories]'):
        query = query + f"filters[categories]={request.GET.get('filters[categories]')}"
    if request.GET.get('q'):
        query = query + f"&q={request.GET.get('q')}"
    if request.GET.get('sort'):
        query = query + f"&sort={request.GET.get('sort')}"
    if request.GET.get('filters[price_amount_lte]'):
        query = query + f"&filters[price_amount_lte]={request.GET.get('filters[price_amount_lte]')}"
    if request.GET.get('filters[price_amount_gte]'):
        query = query + f"&filters[price_amount_gte]={request.GET.get('filters[price_amount_gte]')}"
    if request.GET.get('offset'):
        query = query + f"&offset={request.GET.get('offset')}"
    res = requests.get(f"{OFFER_API}search-results?{query}", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)


def categoriesRoots(request):
    res = requests.get(f"{OFFER_API}categories/roots", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)


def categoriesTree(request):
    res = requests.get(f"{OFFER_API}categories/tree", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)


def Categories(request, id):
    res = requests.get(f"{OFFER_API}categories/{id}", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)


def getOffers(request, id):
    res = requests.get(f"{OFFER_API}offers/{id}", auth=(OFFER_USERNAME, OFFER_PASSWORD)).json()
    return JsonResponse(res)
