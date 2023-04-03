import datetime
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.views.generic.edit import CreateView
from news_paper.models import Post, User, BaseRegistrationForm, Appointment, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.cache import cache

from .models import Category

# @receiver(user_signed_up, dispatch_uid='123')
# def send_greetings(request, user, **kwargs):
#     send_mail(subject='Регистрация', message=f'{user.username}, приветствуем вас на сайте.', recipient_list=['max1001@yandex.ru'], 
#               from_email=None, fail_silently=False)


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
    
    def get_object(self, queryset=None):
        obj = cache.get(self.model.pk, None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(self.model.pk, obj)
        return obj   


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    redirect_field_name = '/news/'
    permission_required = 'news_paper.add_post'
    success_url = '/news/'
    
    def post(self, request, *args, **kwargs):
        category_id = int(request.POST['category'])
        
        post = Post(author=Author.objects.get(id=int(request.POST['author'])), record=request.POST['record'],
             title=request.POST['title'],
             rating=int(request.POST['rating']),
             text=request.POST['text']
             )

        post.save()
        
        Category.objects.get(id=category_id).post_set.add(post)

        for i in Category.objects.get(id=category_id).subscribers.all().values():
                    
            html_content = render_to_string('subscribe_mail.html', {'user': i['username'], 
                                                                    'text': post.text,
                                                                    'ref': post.pk})
            msg = EmailMultiAlternatives(
                subject=f'{post.title} {post.date_time.strftime("%Y-%M-%d")}',
                from_email='zhma-kin@yandex.ru',
                to=[i['email']],
                )
            msg.attach_alternative(html_content, "text/html")
            
            msg.send()
            
        return redirect('/news/')
     
    
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    redirect_field_name = '/'
    permission_required = 'news_paper.change_post'
    success_url = '/news/'
    
    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not (request.user.groups.filter(name='authors').exists() and 
            request.user.id in Author.objects.values_list('user_id', flat=True)):
        authors.user_set.add(user)
        u = Author(user=user, rating=7)
        u.save()
    return redirect('/news/')


@login_required
def deathor(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists() and request.user.id in Author.objects.values_list('user_id', flat=True):
        authors.user_set.remove(user)
        user.author.delete()
    return redirect('/news/')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    redirect_field_name = '/'
    permission_required = 'news_paper.delete_post'
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not (self.request.user.groups.filter(name='authors').exists() 
                                    and self.request.user.id in Author.objects.values_list('user_id', flat=True))
        
                                    
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegistrationForm
    redirect_field_name = '/'


class SubscribeView(View):
    
    def post(self, request: HttpRequest, *args, **kwargs):
        
        user_id = request.user.pk
        cat_id = request.POST.get('category', None)
        u = User.objects.get(id=user_id)
        c = Category.objects.get(id=cat_id)
        c.subscribers.add(u)
        return redirect('/news/')
        
        
class UnsubscribeView(View):
    
    def post(self, request: HttpRequest, *args, **kwargs):
        user_id = request.user.pk
        cat_id = request.POST.get('category', None)
        category_object = Category.objects.get(id=cat_id)
        User.objects.get(id=user_id).category_set.remove(category_object)
        return redirect('/news/')
