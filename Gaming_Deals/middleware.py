from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from news.models import News
from adminpanel.models import Product
User = get_user_model()


class ProjectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('theme', None) is None:
            request.session['theme'] = 'dark'
        response = self.get_response(request)
        return response


class MiddlewareAgentsInfo(MiddlewareMixin):

    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.user_ip = ip
        if request.path:
            if request.user.is_authenticated and request.user.is_superuser:
                request.totalUser = User.objects.all()
                request.totalNews = News.objects.all()
                request.products = Product.objects.all()
        return None
