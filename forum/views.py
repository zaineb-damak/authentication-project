from forum.models import Post,CustomUser
from forum.serializers import PostSerializer,UserSerializer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer


class PostList(generics.ListCreateAPIView):
    queryset  = Post.objects.all()
    serializer_class = PostSerializer
   
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = [JSONRenderer]

class UserList(generics.ListAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
