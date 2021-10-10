from django import forms
from django.forms import ModelForm
from .models import Post,Comment

class PostForm(ModelForm):
    text=forms.CharField(widget=forms.Textarea(attrs={'rows':4}))
    class Meta:
        model=Post
        fields=['text','image']
class CommentForm(ModelForm):
    body=forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model=Comment
        fields=('body',)