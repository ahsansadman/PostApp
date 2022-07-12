from django.urls import path

from .views import HomeView, PostView, PostCreateView, PostUpdateView, PostDeleteView, CommentDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<pk>/<slug:slug>', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
