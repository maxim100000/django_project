import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news_paper.models import Post

class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = datetime.date.today()
        return context

class New(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    
    
    