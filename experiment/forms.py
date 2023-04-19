from django import forms
from .models import Response, Announcement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DeleteAuthorForm(forms.Form):
    name = forms.CharField(max_length=20)
    
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('content','announcement')
        exclude = ['user']
        
        
class CreateForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['user']
        
        

        
        
