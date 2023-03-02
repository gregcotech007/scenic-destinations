"""
Admin file for management of Admin backend
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin Post View with Summernote
    """
    list_display = ('title', 'id', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')
    actions = ['publish_posts']

    def publish_posts(self, request, queryset):
        """
        Publish posts
        """
        queryset.update(status=1)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin Comment View with Model Admin
    """
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """
        Approve comments
        """
        queryset.update(approved=True)
