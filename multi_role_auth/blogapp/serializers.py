from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author']
        extra_kwargs = {'author': {'read_only': True}}  # Make 'author' auto-assigned

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user  # Assign logged-in user
        return super().create(validated_data)

    