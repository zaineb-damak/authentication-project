from forum.models import Post,CustomUser
from forum.serializers import PostSerializer,UserSerializer,MyTokenObtainPairSerializer
from rest_framework import generics, permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_api_key.permissions import HasAPIKey

 





class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PostList(generics.ListAPIView):
    queryset  = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   


class PostCreate(generics.CreateAPIView):
    uthentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset  = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        
   
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [HasAPIKey]


class UserListCreate(generics.ListCreateAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = UserSerializer
    
        

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

