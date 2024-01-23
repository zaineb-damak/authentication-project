from rest_framework import serializers
from forum.models import Post, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username

        return token

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id','title','content','author','created']
    
class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password','email', 'posts', 'api_keys']

    def get_posts(self, obj):
        # Retrieve the posts related to the user 
        posts = obj.post_set.all()
        # Serialize the posts using the PostSerializer
        serializer = PostSerializer(posts, many=True)
        return serializer.data