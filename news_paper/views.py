import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from news_paper.models import Post
from .filters import PostFilter
from .forms import PostForm

class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = datetime.date.today()
        context['categories'] = Post.objects.values_list('category__name', flat=True).distinct()
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class FilterNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class New(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    
   
class PostAddView(CreateView):
    template_name = 'add.html'
    form_class = PostForm
    
 
class PostUpdateView(UpdateView):   
    template_name = 'edit.html'
    form_class = PostForm
    success_url = '/news/'
    
    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
class PostDeleteView(DeleteView):
    template_name = 'delete.html'    
    queryset = Post.objects.all()
    success_url = '/news/'