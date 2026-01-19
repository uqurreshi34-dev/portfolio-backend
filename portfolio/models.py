from django.utils.text import slugify
from django.db import models

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# This configures metadata (settings) for your model - how Django should handle it.
# What ordering = ['-created_at'] Does:

# Automatically sorts all queries by created_at in descending order (newest first)
# The - means descending (reverse order)

# Example:
# python# Without Meta ordering, you'd need to do:
# projects = Project.objects.all().order_by('-created_at')

# # With Meta ordering, this happens automatically:
# projects = Project.objects.all()  # Already sorted newest first!


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=0)  # 0-100
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    # SlugField is a special field type in Django that is used to store URL-friendly versions of text (usually titles).
    slug = models.SlugField(unique=True, blank=True)  # See expn below
    author = models.CharField(
        max_length=100, default="John Doe")  # Change to your name
    excerpt = models.TextField(
        max_length=300, help_text="Short description (max 300 chars)")
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/', blank=True, null=True)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    reading_time = models.IntegerField(
        default=5, help_text="Estimated reading time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
# the save() method you see in your BlogPost model is the built-in
# Django method that every model inherits from models.Model.
# You are overriding (extending) it to add your custom logic.
# What is save()?        → The method that actually writes the model to the database
# What are we doing?     → Adding automatic slug generation before saving
# self.slug?             → The slug field of this particular blog post
# slugify()?             → Django helper: "My Cool Post" → "my-cool-post"
# super().save()?        → Very important! Calls the original save() so the object actually gets saved

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # without this nothing saved to db


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, help_text="Lucide icon name (e.g., 'Code', 'Palette', 'Server')")
    price_range = models.CharField(
        max_length=100, blank=True, help_text="e.g., '$500 - $2000'")
    delivery_time = models.CharField(
        max_length=100, blank=True, help_text="e.g., '1-2 weeks'")
    features = models.TextField(help_text="One feature per line")
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]
        # It takes "SEO, Fast Delivery, Responsive Design"
        # Returns ["SEO", "Fast Delivery", "Responsive Design"]


class SocialPost(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('medium', 'Medium'),
        ('dev', 'Dev.to'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    content = models.TextField()
    url = models.URLField()
    posted_at = models.DateTimeField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0, blank=True)
    image_url = models.URLField(blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.platform} post - {self.posted_at.strftime('%Y-%m-%d')}"


# A ForeignKey creates a many-to-one relationship between two models.
# In this case:
# Many Comments can belong to one BlogPost
# Each Comment "points to" exactly one BlogPost

# In database terms:
# Django will automatically create a column in the Comment table called something like post_id
# This column stores the primary key (usually the id) of the related BlogPost
# This is how Django knows which comments belong to which blog post

# What does on_delete=models.CASCADE mean?
# This setting tells Django what to do with the comments when the blog post they belong to is deleted.
# CASCADE = "delete everything that depends on me"
# Behavior:
# textWhen you do:   blog_post.delete()

# What happens:
# 1. The BlogPost is deleted
# 2. Django automatically finds ALL comments where post_id == that blog_post.id
# 3. Django deletes ALL those comments too

# class Experience(models.Model):
#     EXPERIENCE_TYPE = [
#         ('work', 'Work'),
#         ('education', 'Education'),
#         ('certification', 'Certification'),
#     ]

#     type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE)
#     title = models.CharField(max_length=200)  # Job title or Degree
#     company = models.CharField(max_length=200)  # Company or Institution
#     location = models.CharField(max_length=200)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)  # Null if current
#     current = models.BooleanField(default=False)
#     description = models.TextField()
#     achievements = models.TextField(blank=True)
#     logo = models.ImageField(upload_to='experience/', blank=True)
#     order = models.IntegerField(default=0)


# Why a list of tuples?
# EXPERIENCE_TYPE = [
#     ('work', 'Work'),
#     ('education', 'Education'),
#     ('certification', 'Certification'),
# ]
# This is a list (square brackets []) containing tuples (parentheses ()).
# Each tuple has two values:

# First value ('work', 'education', 'certification') - what gets stored in the database
# Second value ('Work', 'Education', 'Certification') - what gets displayed to humans (in admin panel, forms, etc.)


# Why Tuples Instead of a Simple List?
# Django uses this pattern for choices in model fields. It needs two pieces of information:
# Database Value (Internal)

# Short, lowercase, no spaces
# Good for code and database storage
# Example: 'work'

# Display Value (Human-readable)

# Friendly, capitalized, readable
# Shows up in forms and admin interface
# Example: 'Work'


# How It Works
# pythontype = models.CharField(max_length=20, choices=EXPERIENCE_TYPE)
# ```

# When you use this field:

# **In the database:**
# ```
# | id | type      | title           |
# |----|-----------|-----------------|
# | 1  | work      | Software Dev    |
# | 2  | education | Computer Science|
# | 3  | work      | Freelancer      |
# In Django Admin:
# You see a dropdown with:

# Work
# Education
# Certification

# In your code:
# pythonexp = Experience.objects.get(id=1)
# print(exp.type)  # Output: 'work'
# print(exp.get_type_display())  # Output: 'Work'  ← Django magic method!

# Why Not Just Use Strings?
# Bad approach:
# pythontype = models.CharField(max_length=20)  # No choices
# Problems:

# Users could type anything: "wrk", "WORK", "job", etc.
# Inconsistent data
# Hard to query
# No validation

# Good approach (with choices):
# pythontype = models.CharField(max_length=20, choices=EXPERIENCE_TYPE)
# Benefits:

# ✅ Only valid values allowed
# ✅ Consistent data
# ✅ Easy to query: Experience.objects.filter(type='work')
# ✅ Nice dropdown in admin
# ✅ Can display human-readable labels


# Real-World Example
# python# Create an experience
# exp = Experience.objects.create(
#     type='work',  # Store 'work' in database
#     title='Senior Developer',
#     company='Tech Corp'
# )

# # In your API response
# {
#     "type": "work",  # Database value
#     "type_display": "Work",  # Human-readable (use get_type_display())
#     "title": "Senior Developer"
# }

# Could You Use Other Data Structures?
# Yes, but tuples are standard:
# python# List of tuples (standard, recommended)
# CHOICES = [('val1', 'Display 1'), ('val2', 'Display 2')]

# # Tuple of tuples (also works)
# CHOICES = (('val1', 'Display 1'), ('val2', 'Display 2'))

# # List of lists (works but ugly)
# CHOICES = [['val1', 'Display 1'], ['val2', 'Display 2']]
# Django convention is list of tuples because:

# Tuples are immutable (can't be accidentally changed)
# Each choice pair should never change
# More memory efficient


# Summary
# Q: Why tuples?
# A: To separate what's stored (database value) from what's displayed (human label)
# Q: Why a list of tuples?
# A: Multiple choices, each with two values
# Q: Could it be something else?
# A: Technically yes, but list of tuples is Django's standard pattern for choices


# What does a slug look like?
# Normal title:
# "My First Awesome Blog Post!!!"
# Slug (after slugify):
# my-first-awesome-blog-post
# So the URL becomes something beautiful like:
# https://yoursite.com/blog/my-first-awesome-blog-post/
# instead of the ugly version:
# https://yoursite.com/blog/?id=47 or https://yoursite.com/blog/post/47
# Main characteristics of SlugField

# Only allows safe characters, letters, numbers, hyphens, underscores
# usually lowercase - slugify converts to lowercase
# replaces spaces with -
# removes special characters
# Unique (most often) so 2 posts cant have the same slug
# not meant for humans to type, its generated automatically from title, but looks nice when shared,
# people copy-paste it from browser
