from django.urls import path,include
from forum import views

urlpatterns = [
    path('forum/', views.PostList.as_view()),
    path('forum/<int:pk>', views.PostDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),

]