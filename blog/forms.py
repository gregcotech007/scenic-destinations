from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'featured_image')
