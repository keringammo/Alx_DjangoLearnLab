from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Search posts
    path('search/', views.search_posts, name='search-posts'),

    # Filter posts by tag
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),
]


