from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Project, Skill, Contact, BlogPost,
                     Service, SocialPost, Comment)
from .serializers import (ProjectSerializer, SkillSerializer,
                          ContactSerializer, BlogPostListSerializer,
                          BlogPostDetailSerializer, ServiceSerializer,
                          SocialPostSerializer, CommentSerializer)

# Create your views here.
# Class based views


class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SkillListView(ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ContactCreateView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class BlogPostListView(ListAPIView):
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        queryset = BlogPost.objects.filter(published=True)
        category = self.request.query_params.get('category', None)
        featured = self.request.query_params.get('featured', None)

        if category:
            queryset = queryset.filter(category__iexact=category)
        if featured:
            queryset = queryset.filter(featured=True)

        return queryset


class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        # calling method on RetrieveAPIView class
        obj = super().get_object()

        # Increment views after object is successfully retrieved
        # see expn below for F
        BlogPost.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        obj.refresh_from_db()

        return obj


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class SocialPostListView(ListAPIView):
    serializer_class = SocialPostSerializer

    def get_queryset(self):
        queryset = SocialPost.objects.all()
        platform = self.request.query_params.get('platform', None)
        limit = self.request.query_params.get('limit', None)

        if platform:
            queryset = queryset.filter(platform=platform)
        if limit:
            queryset = queryset[:int(limit)]

        return queryset


class BlogCategoriesView(APIView):
    """Get list of all blog categories"""

    def get(self, _request):
        categories = BlogPost.objects.filter(
            published=True).values_list('category', flat=True).distinct()
        return Response(list(categories))


#  What is F('views') + 1?
# F() is a very useful Django expression from django.db.models — it lets you do database-level atomic updates without race conditions.
# Without F():
# Pythonpost = BlogPost.objects.get(pk=obj.pk)
# post.views = post.views + 1          # ← reads current value
# post.save()                          # ← writes back
# Problem: If two users view the page at the exact same time → both read the same value → both write old + 1 → only +1 total instead of +2 (race condition).
# With F():
# PythonBlogPost.objects.filter(pk=obj.pk).update(views=F('views') + 1)

# F('views') → "refer to the current value of the views column in the database"
# + 1 → tell the database: "add 1 to whatever is currently there"
# .update() → single SQL query: UPDATE ... SET views = views + 1 WHERE pk = ...
# Atomic — database handles it safely, no race condition even with 1000 concurrent views

# Then obj.refresh_from_db() reloads the object so obj.views reflects the new value (useful if you return the object in the response).
