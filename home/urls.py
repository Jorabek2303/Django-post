from django.urls import path
from .views import *

urlpatterns = [
    path('',HomeView,name='home'),
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('register/',RegisterView,name='register'),
    path('profile/<int:pk>/',ProfileView,name='profile'),
    path('create-post/<int:pk>/',CreatePostView,name='create_post'),
    path('posts/<int:pk>',PostsView,name='posts'),
    path('edit-post/<int:pk>',EditpostView,name='edit_post'),
    path('delete-post/<int:pk>',DeletepostView,name='delete_post'),
    path('comment/<int:pk>',CommentView,name='comment'),
    path('edit-comment/<int:pk>',EditCommentView,name='edit_comment')
]