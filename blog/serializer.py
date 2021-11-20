from rest_framework.serializers import ModelSerializer
from .models import Comment, Post
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content','image']

class DisplayPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','image','author']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class LoginSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['username','password']