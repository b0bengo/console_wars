from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blog/post.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()

        # Get filter parameters from the request
        console_filter = self.request.GET.get('console', None)
        sort_order = self.request.GET.get('sort', None)

        # Filter by console
        if console_filter:
            queryset = queryset.filter(author__useroption__option=console_filter)

        # Sort by date
        if sort_order == 'oldest':
            queryset = queryset.order_by('created_on')
        elif sort_order == 'newest':
            queryset = queryset.order_by('-created_on')

        return queryset

class UserPostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/blog/user_posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike the post
    else:
        post.likes.add(request.user)  # Like the post
    return redirect('post_list')  # Redirect to the posts list or any other appropriate page

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post_detail', pk=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:  # Ensure the logged-in user is the author
        comment.delete()
        return redirect('post_detail', pk=comment.post.id)
    else:
        return redirect('post_detail', pk=comment.post.id)  # Redirect if unauthorized

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('user_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('user_posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()  # Fetch all comments for the post
        return context