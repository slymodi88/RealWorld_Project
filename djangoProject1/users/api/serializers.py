import jwt
from rest_framework import serializers

from djangoProject1 import settings
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if not user.auth_token:
            data = {
                "id": user.id,
                "email": user.email

            }
            auth_token = {'token': jwt.encode(
                data, settings.SECRET_KEY)}
            user.auth_token = bytes.decode(auth_token['token'])
            user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
