from rest_framework import serializers

from realworld.models import Article, Comment, Tag, UserArticleFavorites


# class CommentSerializerList(serializers.ModelSerializer):
#     body = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.user_name
        return data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.user_name
        data["comments"] = Comment.objects.filter(article=instance).values("body")
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class UserArticleFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArticleFavorites
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.user_name
        return data
