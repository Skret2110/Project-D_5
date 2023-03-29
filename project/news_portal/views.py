from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import News
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsDetail(DetailView):
    model = News
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_news',)
    #raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_news',)
    model = News
    template_name = 'news_delete.html'
    queryset = News.objects.all()
    success_url = reverse_lazy('news_list')


class NewsSearch(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context