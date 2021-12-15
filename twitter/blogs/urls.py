from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('createPost/', views.createPost, name = 'createPost'),    
    path('deletePost/<int:post_pk>', views.deletePost, name = 'deletePost'),
    path('updatePost/<int:post_pk>', views.updatePost, name = 'updatePost'),
    path('getPostsFromTags/', views.getPostsFromTags, name = 'getPostsFromTags'),
    path('getPostsFromText/', views.getPostsFromText, name = 'getPostsFromText'),
    path('getPostsFromDates/', views.getPostsFromDates, name = 'getPostsFromDates'),
    path('createPostForm/', views.createPostForm, name='createPostForm'),
    path('getPostsByForm/', views.getPostsByForm, name = 'getPostsByForm'),
]