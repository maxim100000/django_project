import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView 
from django.views.generic.edit import CreateView
from news_paper.models import Post, User, BaseRegistrationForm
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class News(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm
    redirect_field_name = '/'
    
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


class FilterNews(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10
    redirect_field_name = '/'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    
class New(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    redirect_field_name = '/'
    permission_required = 'news_paper.view_post'
    
   
class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    redirect_field_name = '/'
    permission_required = 'news_paper.add_post'
    
    
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    redirect_field_name = '/'
    permission_required = 'news_paper.change_post'
    
 
    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 

@login_required
def upgrade_me(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(user)
    return redirect('/news/')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'    
    queryset = Post.objects.all()
    redirect_field_name = '/'
    permission_required = 'news_paper.delete_post'
    
    
class IndexView(LoginRequiredMixin, TemplateView):    
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):    
    model = User
    form_class = BaseRegistrationForm
    redirect_field_name = '/'
