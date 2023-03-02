"""
File for Forms, Posts and Comments
"""
from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """
    Comment form
    """
    class Meta:
        """
        Comment model with field of body
        """
        model = Comment
        fields = ('body',)


class ImageUploadForm(forms.ModelForm):
    """
    Image upload form
    """
    class Meta:
        """
        Image upload form with title, content and featured image
        """
        model = Post
        fields = ('title', 'content', 'featured_image')
