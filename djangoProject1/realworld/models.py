from django.db import models

# Create your models here.
from mixins.models import Timestamps


class Article(Timestamps):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.ManyToManyField("Tag", through="ArticleTag")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Article'


class Comment(Timestamps):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.body

    class Meta:
        verbose_name_plural = 'Comment'


class Tag(Timestamps):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Tag'


class ArticleTag(Timestamps):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Article Tag'


class UserArticleFavorites(Timestamps):
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    article = models.ForeignKey("Article", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'User Favorite Articles'
