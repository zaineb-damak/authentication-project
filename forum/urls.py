from django.urls import path,include
from forum import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(),name='post-detail'),
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
