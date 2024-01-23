from forum.models import Post,CustomUser
from forum.serializers import PostSerializer,UserSerializer,MyTokenObtainPairSerializer
from rest_framework import generics, permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simple_api_key.permissions import IsActiveEntity
from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework_simple_api_key.permissions import IsActiveEntity
from rest_framework_simple_api_key.models import APIKey
 





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
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsActiveEntity]


class UserListCreate(generics.ListCreateAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = UserSerializer

    
    def create_api_key(self, custom_user):
        obj, key = APIKey.objects.create_api_key(entity=custom_user)  # Adjust the method call based on your actual implementation
        return {"key": key}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        custom_user = serializer.instance

        result = self.create_api_key(custom_user)

        headers = self.get_success_headers(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

        

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

