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
