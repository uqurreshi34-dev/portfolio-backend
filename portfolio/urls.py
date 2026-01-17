from django.urls import path
from .views import ProjectListView, ProjectDetailView, SkillListView, ContactCreateView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
]
