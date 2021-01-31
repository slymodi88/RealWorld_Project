from django.urls import path

from realworld.api.views import ArticleApi, CommentApi, ArticleApiDetails, CommentApiDetails, TagApiList, \
    UserArticleFavoritesList, UserArticleFavoritesDetails

urlpatterns = [
    path('', ArticleApi.as_view(), name='Article'),
    path('<int:pk>/', ArticleApiDetails.as_view(), name='Article'),
    path('comment/', CommentApi.as_view(), name='Comment'),
    path('comment/<int:pk>/', CommentApiDetails.as_view(), name='Comment'),
    path('tags/', TagApiList.as_view(), name='Tag'),
    path('favorite/', UserArticleFavoritesList.as_view(), name='UserArticleFavourites'),
    path('favorite/<int:id>/', UserArticleFavoritesDetails.as_view(), name='UserArticleFavourites'),



]
