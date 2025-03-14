from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
     path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('user_posts/', views.UserPostList.as_view(), name='user_posts'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
]