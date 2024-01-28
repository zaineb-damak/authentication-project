from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from forum.models import Post
from rest_framework_api_key.models import APIKey


class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
    def test_get_access_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_authenticated_user(self):
        response_token = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        token=response_token.data['access']

        response = self.client.get('/posts/',HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cerate_post_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        data = {"title":"test post", "content":"test content"}
        response = self.client.post("/posts/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail_allows_authenticated_user(self):
        _, key = APIKey.objects.create_key(name="test")
        authorization = f"Api-Key {key}"
        post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        response = self.client.get(f'/posts/{post.pk}/',HTTP_AUTHORIZATION=authorization)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


