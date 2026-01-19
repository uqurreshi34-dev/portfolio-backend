from rest_framework import serializers
from .models import (Project, Skill, Contact, Comment,
                     BlogPost, Service, SocialPost)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'comment', 'created_at']
        read_only_fields = ['created_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for blog list (without full content)"""
# comments_count is not a real field in the BlogPost model.
# We want to show how many approved comments each post has.
# SerializerMethodField() tells DRF: "I'll calculate this value myself using a method".
# Django rest framework will automatically look for a method called get_comments_count
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'featured_image',
            'category', 'tags', 'views', 'reading_time', 'created_at',
            'updated_at', 'featured', 'comments_count'
        ]  # notice - no 'comments' field as expnd above

    # This method runs automatically for every blog post when the serializer is used.
# obj → the current BlogPost object being serialized (e.g. one post from the queryset)
# obj.comments → uses the reverse relationship from your Comment model
# (because you have post = models.ForeignKey(BlogPost, related_name='comments', ...)
# .filter(approved=True) → only count comments that are approved (nice safety!)
# .count() → returns the number (e.g. 5)

# So if a post has 7 approved comments → comments_count: 7 appears in the JSON.

    def get_comments_count(self, obj):
        return obj.comments.filter(approved=True).count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for single blog post (with full content)"""
    comments = serializers.SerializerMethodField()
    # not a field in BlogPost model - django rest framework will look for get_comments method

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'content',
            'featured_image', 'category', 'tags', 'views', 'reading_time',
            'created_at', 'updated_at', 'comments'
        ]

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(approved=True)
        return CommentSerializer(approved_comments, many=True).data


class ServiceSerializer(serializers.ModelSerializer):
    features_list = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'description', 'icon', 'price_range',
            'delivery_time', 'features', 'features_list', 'featured', 'order'
        ]

    def get_features_list(self, obj):
        return obj.get_features_list()  # Method in the service class


class SocialPostSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(
        source='get_platform_display', read_only=True)
    # SocialPost has a field called platform defined with choices= then
    # then Django automatically creates the method get_platform_display() for you behind the scenes.
    # behind the scenes Django does this: return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)
    # 1st arg is Key, 2nd arg is fallback e.g if our dict doesnt have key 'old-platform' our fallback will be
    # old-platform (raw value) returned by .get().. if our dict has instagram key our get() will return
    # Instagram (nice display name)
    # .get(self.platform, self.platform) twice because We never want get_platform_display() to return None
    # — better to show the raw value than nothing

    class Meta:
        model = SocialPost
        fields = [
            'id',
            'platform',
            'platform_display',
            'content',
            'url',
            'posted_at',
            'likes',
            'comments',
            'shares',
            'image_url',
            'fetched_at'
        ]
