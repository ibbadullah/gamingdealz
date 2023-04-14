from news.models import News


def djangoGoble(request):
    return {'GNews': News.objects.all()}
