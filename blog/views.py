from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blog/indexpost.html'
    context_object_name = 'posts'

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')