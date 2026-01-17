"""
URL configuration for portfolio_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# What It Does:
# "If we're in development mode, let Django serve uploaded files (like images) directly."
# Line by Line:
# if settings.DEBUG:

# "If we're in development mode (DEBUG = True)"
# DEBUG is True when you're coding on your laptop
# DEBUG is False when your site is live/in production

# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Creates a URL pattern that serves files from your media folder
# MEDIA_URL = '/media/' → The URL path
# MEDIA_ROOT = 'path/to/media' → The actual folder on your computer

# Real Example:
# Let's say a user uploads a profile picture called avatar.jpg:

# Django saves it to: backend/media/profiles/avatar.jpg
# This code creates a URL: http://localhost:8000/media/profiles/avatar.jpg
# When you visit that URL, Django serves the image

# Why "if DEBUG"?
# In development (your laptop):

# Django handles serving images ✅
# Easy and convenient

# In production (live server):

# Django should NOT serve images ❌
# It's slow and inefficient
# Use a proper file server like AWS S3, Cloudinary, or Nginx instead
