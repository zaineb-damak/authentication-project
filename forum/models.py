from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from forum.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length = 250)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,) 
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


