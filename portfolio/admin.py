from django.contrib import admin
from .models import (Project, Skill, Contact, BlogPost,
                     SocialPost, Service, Comment)

# register your models here


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'created_at']
    list_filter = ['featured', 'created_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    # This forces newest first in the admin change list
    ordering = ['-created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author',
                    'published', 'featured', 'views', 'created_at']
    list_filter = ['published', 'featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['published', 'featured']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    list_editable = ['approved']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order', 'created_at']
    list_filter = ['featured', 'created_at']
    list_editable = ['featured', 'order']


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ['platform', 'posted_at',
                    'likes', 'comments', 'shares', 'fetched_at']
    list_filter = ['platform', 'posted_at']
    ordering = ['-posted_at']
