from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm ):

    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'image', 'category']

        widgets = {
            'title':forms.TimeInput(attrs={'class':'form-control'}),
            'excerpt':forms.Textarea(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
        }
