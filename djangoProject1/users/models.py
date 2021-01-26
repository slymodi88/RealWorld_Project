from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
from mixins.models import Timestamps


class User(AbstractBaseUser):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    auth_token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "user_name"

    class Meta:
        verbose_name_plural = 'User'


class Follow(Timestamps):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    follow = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_follow")

    class Meta:
        verbose_name_plural = 'Follow'
