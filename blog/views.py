"""
File for Blog App Views
"""
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post, Comment
from .forms import CommentForm, ImageUploadForm


class PostListView(ListView):
    """
    View to list all posts in an order that is paginated, 6 posts max per pages
    """
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_on']
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')


class UserPostListView(ListView):
    """
    View to list all User posts in an order that is paginated, 6 posts max
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_on')


class PostDetailView(DetailView):
    """
    View to post details
    """
    model = Post

    def get(self, request, pk, *args, **kwargs):
        """
        View to show post details to user
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, pk=pk)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        author = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if request.user.is_authenticated:
            if post.author == request.user:
                author = True

        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
                "author": author
            },
        )

    def post(self, request, pk, *args, **kwargs):
        """
        Post to filter approved comments by created on and show likes if true
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, pk=pk)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View to list all posts in an order that is paginated, 6 posts max per pages
    """
    model = Post
    form_class = ImageUploadForm
    success_url = '/'
    success_message = 'Post successfully submitted for review'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin,
                     UserPassesTestMixin, UpdateView):
    """
    View to update post
    """
    model = Post
    form_class = ImageUploadForm
    success_url = '/'
    success_message = 'Post successfully updated'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin,
                     UserPassesTestMixin, DeleteView):
    """
    User can delete post
    """
    model = Post
    success_url = '/'
    success_message = 'Post successfully deleted'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostLike(View):
    """
    User can like or unlike a post
    """
    def post(self, request, pk):
        """
        A view to display a like or unlike on the post
        """
        post = get_object_or_404(Post, pk=pk)

        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post-detail', args=[pk]))


class UserCommentListView(ListView):
    """
    View a list for user comments on post
    """
    model = Post
    template_name = 'blog/user_comments.html'
    context_object_name = 'comments'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Comment.objects.filter(
            name=user.username).order_by('-created_on')


class CommentDeleteView(LoginRequiredMixin,
                        SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    """
    User can delete an comment of their own
    """
    model = Comment
    success_url = '/'
    success_message = 'Comment successfully deleted'

    def test_func(self):
        comment = self.get_object()
        if self.request.user.username == comment.name:
            return True
        return False
