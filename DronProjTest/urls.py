"""
URL configuration for DronProjTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from experiment.views import CreateAnnouncement, UpdateAnnouncement, DeleteAnnouncement, Preview,\
register, regend, accept, reject, check_code, Detail, AnnouncementResponse, get_users_records
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', CreateAnnouncement.as_view(template_name='announcement_form.html'), name='create'),
    path('update/<slug:pk>', UpdateAnnouncement.as_view(template_name='announcement_update_form.html'), name='update'),
    path('delete/<slug:pk>', DeleteAnnouncement.as_view(template_name='announcement_confirm_delete.html')),
    path("preview/", Preview.as_view(), name='preview'),
    path("detail/<slug:pk>", Detail.as_view(), name='detail'),
    path("login/", LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", register, name='register'),
    path("regend/", regend, name='regend'),
    path("check/", check_code, name='check'),
    path("response/", AnnouncementResponse.as_view(), name='response'),
    path("usersrec/", get_users_records, name='usersrec'),
    path("accept/<int:pk>", accept, name='accept'),
    path("reject/<int:pk>", reject, name='reject'),
]
