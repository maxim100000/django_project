import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from DronProjTest import settings
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Announcement, Response, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ResponseForm, CreateForm
from .filters import AnnouncementFilter


class Preview(ListView):
    model = Announcement
    template_name = 'preview.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class Detail(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'announcement_detail.html'


class AnnouncementResponse(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'announcement_response.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            Response.objects.create(content=request.POST['content'],
                                    announcement=Announcement.objects.get(id=request.POST['announcement']),
                                    user=User.objects.get(id=request.user.id))
            email = Announcement.objects.get(id=request.POST.get('announcement')).user.email
            send_mail(subject='Отзыв', message='Есть новый отзыв', from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[email])
        return redirect('/preview/')


class CreateAnnouncement(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = CreateForm

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            Announcement.objects.create(title=request.POST['title'],
                                        category=Category.objects.get(id=request.POST['category']),
                                        user=User.objects.get(id=request.user.id), content=request.POST['content'])
        return redirect('/preview/')


class UpdateAnnouncement(LoginRequiredMixin, UpdateView):
    model = Announcement
    fields = ['title', 'content', 'category']


class DeleteAnnouncement(LoginRequiredMixin, DeleteView):
    model = Announcement


def register(request):
    if not request.user.is_authenticated:
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    else:
        return redirect('/preview/')


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


def regend(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.fields)
        if form and form.is_valid():
            request.session['form'] = form.cleaned_data
            print(request.session.get('form'))
            code = generate_code()
            send_mail(subject='Код', message=code, from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[form.cleaned_data['email']])
            request.session['code'] = code
            print(request.session['code'])
            return render(request, 'registration/enter_code.html')
        else:
            return redirect('/register/')


def check_code(request):
    if request.POST['code'] == request.session.get('code'):
        form = request.session.get('form')
        User.objects.create(password=make_password(form['password1']), username=form['username'],
                            email=form['email'])
    return redirect('/preview/')


@login_required
def get_users_records(request):
    f = AnnouncementFilter(request.GET, queryset=User.objects.get(id=request.user.id).announcement_set.all())
    return render(request, 'users_announcement.html', {'filter': f})


@login_required
def accept(request, pk):
    send_mail(subject='Про отзыв', message='Ваш отзыв принят', from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[Response.objects.get(id=pk).user.email])
    responce_obj = Response.objects.get(id=pk)
    responce_obj.accepted = True
    responce_obj.save()
    return redirect('usersrec')


@login_required
def reject(request, pk):
    Response.objects.get(id=pk).delete()
    return redirect('usersrec')
