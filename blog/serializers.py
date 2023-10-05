from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost, Like, Comment

class BlogPostSerializer(serializers.ModelSerializer):


    # image_url = serializers.SerializerMethodField(read_only=True)
    post_url = serializers.HyperlinkedIdentityField('post_get_update')
    
    class Meta:
        model = BlogPost
        fields = ("id","title", "content", "author", "image", "post_url")#,"image_url"


    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)
    #     return None

    def create(self, validated_data):
        blog = BlogPost.objects.create(**validated_data)
        return blog

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields ="__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

