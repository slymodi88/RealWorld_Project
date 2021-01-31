from django_redis import cache
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from mixins.paginator import CustomPagination
from realworld.api.serializers import ArticleSerializer, CommentSerializer, TagSerializer, \
    UserArticleFavoritesSerializer
from realworld.models import Article, Comment, Tag, UserArticleFavorites


class ArticleApi(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        # paginator = self.pagination_class()
        queryset =self.paginate_queryset(Article.objects.all())

        serializer = ArticleSerializer(queryset, many=True)
        # return Response({"result": serializer.data, "message": "Done", }, status=201)
        return self.paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except:
            pass
        data["user"] = request.user.id
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)


class ArticleApiDetails(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["pk"])

        serializer = ArticleSerializer(article)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=200)

    def update(self, request, *args, **kwargs):
        data = request.data
        article = get_object_or_404(Article, id=kwargs["pk"])
        if request.user != article.user:
            raise PermissionDenied

        serializer = ArticleSerializer(instance=article, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)

    def delete(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["pk"])
        if request.user != article.user:
            raise PermissionDenied
        article.delete()
        return Response({"message": "Done", "status": True}, status=200)


class CommentApi(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", }, status=201)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except:
            pass
        data["user"] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)


class CommentApiDetails(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs["pk"])
        if request.user != comment.user:
            raise PermissionDenied
        serializer = CommentSerializer(comment)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=200)

    def put(self, request, *args, **kwargs):
        data = request.data
        comment = get_object_or_404(Comment, id=kwargs["pk"])
        print(request.user.id, comment)
        if request.user != comment.user:
            raise PermissionDenied
        try:
            data._mutable = True
        except:
            pass
        # data["article"] = kwargs["pk"]

        serializer = CommentSerializer(instance=comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs["pk"])
        if request.user != comment.user:
            raise PermissionDenied
        comment.delete()
        return Response({"message": "Done", "status": True}, status=200)


class TagApiList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", }, status=201)


class UserArticleFavoritesList(generics.ListCreateAPIView):
    queryset = UserArticleFavorites.objects.all()
    serializer_class = UserArticleFavoritesSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data._mutable = True
        except:
            pass
        data["user"] = request.user.id

        serializer = UserArticleFavoritesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)


class UserArticleFavoritesDetails(generics.RetrieveUpdateAPIView):
    queryset = UserArticleFavorites.objects.all()
    serializer_class = UserArticleFavoritesSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        favorite_article = get_object_or_404(UserArticleFavorites, id=kwargs["id"])
        if request.user != favorite_article.user:
            raise PermissionDenied
        favorite_article.delete()
        return Response({"message": "Done", "status": True}, status=200)

# class ApiArticleListView(ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = (IsAuthenticated,)
#     pagination_class = CustomPagination



