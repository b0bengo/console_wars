from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]