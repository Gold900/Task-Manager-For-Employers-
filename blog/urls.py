from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostAllView, PostUserView


urlpatterns = [

    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog-postdetail'),
    path('post/new/', PostCreateView.as_view(), name='blog-postcreate'),
    path('post/all/', PostAllView.as_view(), name='blog-postall'),
    path('post/<str:username>/', PostUserView.as_view(), name='blog-postuser'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='blog-postupdate'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(template_name='blog/post_delete.html'), name='blog-postdelete'),
    path('about/', views.about, name='blog-about'),

]
