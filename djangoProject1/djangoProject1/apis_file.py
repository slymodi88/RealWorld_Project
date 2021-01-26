from django.urls import path, include

urlpatterns = [
    path('user/', include("users.api.urls")),
    path('article/', include("realworld.api.urls")),
    path('article/comment/', include("realworld.api.urls")),
    path('tags/', include("realworld.api.urls"))
]
