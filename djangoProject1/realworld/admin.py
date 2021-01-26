from django.contrib import admin

# Register your models here.
from realworld.models import Article, Comment, Tag, UserArticleFavorites, ArticleTag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(UserArticleFavorites)
class UserArticleFavoritesAdmin(admin.ModelAdmin):
    list_display = ("id",)
