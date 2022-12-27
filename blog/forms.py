from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('featured_image', 'title', 'content')
