from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blog/post.html'
    paginate_by = 6
    context_object_name = 'posts'

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

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')