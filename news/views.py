from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView
from news.models import News
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test, login_required


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsListView(ListView):
    model = News
    paginate_by = 20
    extra_context = {'page': "News"}

    def get_queryset(self):
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        by = self.request.GET.get('by')
        sort = self.request.GET.get('sort')
        news = self.model.objects.all()
        if status == "active":
            news = news.filter(activate=True)
        if status == "deactivate":
            news = news.filter(activate=False)
        if by == "headline":
            news = news.filter(headline__icontains=search)
        if by == "description":
            news = news.filter(headline__icontains=search)
        if sort == "desc":
            news = news.order_by('-id')
        return news


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsCreateView(CreateView, SuccessMessageMixin):
    template_name = 'news/news_form.html'
    model = News
    fields = ['img', 'headline', 'category', 'dec', 'youtube_url',
              'text', 'button_text1', 'offer_Button', 'link_url1', 'offer', 'activate', 'text2']
    success_url = reverse_lazy('news_list')
    success_message = "%(name)s has created successfully"
    extra_context = {'page': "News"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'news/news_form.html'
    model = News
    fields = ['img', 'headline', 'category', 'dec', 'youtube_url',
              'text', 'button_text1', 'offer_Button', 'link_url1', 'offer', 'activate', 'text2']
    success_url = reverse_lazy('news_list')
    success_message = "%(name)s has Updated successfully"
    extra_context = {'page': "News"}


@login_required
def newDeleteView(request):
    if request.method == "POST":
        try:
            id = request.POST.get("input_del")
            if id:
                news = get_object_or_404(News, pk=id)
                headline = news.headline
                news.delete()
                messages.success(request, f'This {headline} News Deleted...!')
                return redirect('news_list')
        except Exception as e:
            print(e)
            messages.error(request, 'Error on Deleted News')
            return redirect('news-list')
