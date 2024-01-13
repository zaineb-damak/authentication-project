from rest_framework import serializers
from forum.models import Post, CustomUser

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id','title','content','author','created']
    
class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'api_key', 'posts']

    def get_posts(self, obj):
        # Retrieve the posts related to the user (assuming you have a related name in your Post model)
        posts = obj.post_set.all()
        # Serialize the posts using the PostSerializer
        serializer = PostSerializer(posts, many=True)
        return serializer.data