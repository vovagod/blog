from rest_framework import serializers
from django.contrib.auth.models import User
from myblog.models import Post

class PostSerializer(serializers.ModelSerializer):
       class Meta:
        model = Post
        fields = ('id', 'blogger', 'title', 'text', 'posts',
                  'subscriptions', 'readposts', 'time_created')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
