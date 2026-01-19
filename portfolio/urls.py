# portfolio/urls.py
from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, SkillListView, ContactCreateView,
    BlogPostListView, BlogPostDetailView, CommentCreateView,
    ServiceListView, SocialPostListView, BlogCategoriesView
)

urlpatterns = [
    # Existing URLs
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),

    # New URLs
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/categories/', BlogCategoriesView.as_view(), name='blog-categories'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('social/', SocialPostListView.as_view(), name='social-list'),
]
