from Gaming_Deals.utitls import getResponce
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render
from adminpanel.models import Favourite, SearchRecode
from news.models import News


def getFavouriteIds():
    ids_list = ''
    for i in Favourite.objects.all():
        ids_list += i.offer_id + ','
    res = getResponce(f'offers/{ids_list[:-1:]}')
    if res.get('status', '') == 404:
        res = {'items': []}
    return res['items']


class PublicareaIndex(View):
    template_name = "publicarea/index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['categories'] = getResponce("categories/roots")['items']
        self.context['favourite'] = getFavouriteIds()
        return render(request, self.template_name, self.context)


class SearchOffer(View):
    template_name = "publicarea/search-page.html"
    context = {}

    def get(self, request, *args, **kwargs):
        newPart = "&document_types=offer&document_types=product_offer"
        if not request.GET.get('shops'):
            if request.GET.get('search'):
                SearchRecode(title=request.GET.get('search'), ip=request.user_ip).save()
            if not request.GET.get('search') and not request.GET.get('shops'):
                #return render(request, '404.html')
                pass
        q = '?'
        if request.GET.get('search') or request.GET.get('shops'):
            if request.GET.get('shops') and not request.GET.get('shops') is '0':
                q += f"filters[shops]=%5B{request.GET.get('shops')}%5D{newPart}"
            if request.GET.get('search'):
                if request.GET.get('shops'):
                    q += "&"
                q += f"q={request.GET.get('search')}{newPart}"
        if request.GET.get('price_amount_lte'):
            q += f"&filters[price_amount_lte]={request.GET.get('price_amount_lte')}{newPart}"
        if request.GET.get('price_amount_gte'):
            q += f"&filters[price_amount_gte]={request.GET.get('price_amount_gte')}{newPart}"
        if request.GET.get('sort'):
            q += f"&sort={request.GET.get('sort')}{newPart}"
        if request.GET.get('offset'):
            q += f"&offset={request.GET.get('offset')}{newPart}"
        offers = getResponce(f"search-results{q}")
        if request.GET.get('shops'):
            if request.GET.get('shops') is not '0':
                print("Category Meta Data")
        self.context['ShopsList'] = getResponce(f"shops")['items']
        print(self.context['ShopsList'])
        if offers.get('status', '') == 404:
            offers = {'items': []}
        self.context['offers'] = offers
        return render(request, self.template_name, self.context)


class OffersByCategory(View):
    template_name = "publicarea/offers-by-category.html"
    context = {}

    def get(self, request, *args, **kwargs):
        newPart = "&document_types=offer&document_types=product_offer"
        if not request.GET.get('categories'):
            if request.GET.get('search'):
                SearchRecode(title=request.GET.get('search'), ip=request.user_ip).save()
            if not request.GET.get('search') and not request.GET.get('categories'):
                return render(request, '404.html')
        q = '?'
        if request.GET.get('search') or request.GET.get('categories'):
            if request.GET.get('categories') and not request.GET.get('categories') is '0':
                q += f"filters[categories]=%5B{request.GET.get('categories')}%5D{newPart}"
            if request.GET.get('search'):
                if request.GET.get('categories'):
                    q += "&"
                q += f"q={request.GET.get('search')}{newPart}"
        if request.GET.get('price_amount_lte'):
            q += f"&filters[price_amount_lte]={request.GET.get('price_amount_lte')}{newPart}"
        if request.GET.get('price_amount_gte'):
            q += f"&filters[price_amount_gte]={request.GET.get('price_amount_gte')}{newPart}"
        if request.GET.get('sort'):
            q += f"&sort={request.GET.get('sort')}{newPart}"
        if request.GET.get('offset'):
            q += f"&offset={request.GET.get('offset')}{newPart}"
        offers = getResponce(f"search-results{q}")
        if request.GET.get('categories'):
            if request.GET.get('categories') is not '0':
                self.context['cates'] = getResponce(f'/categories/{request.GET.get("categories")}')['items'][0]
        self.context['categories'] = getResponce(f"categories/roots")['items']
        self.context['ShopsList'] = getResponce(f"shops")['items']
        print("Checking Shops!")
        print(self.context['ShopsList'])
        if offers.get('status', '') == 404:
            offers = {'items': []}
        self.context['offers'] = offers
        return render(request, self.template_name, self.context)


class DealsView(View):
    template_name = "publicarea/deals.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['categories'] = getResponce("categories/roots")['items']
        return render(request, self.template_name, self.context)


class NewsDetailView(DetailView):
    template_name = "publicarea/news-details.html"
    model = News


class FavoriteDealsView(View):
    template_name = "publicarea/favorite-deals.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['favorites'] = getFavouriteIds()
        return render(request, self.template_name, self.context)
