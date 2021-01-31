from django.urls import path

from users.api.views import UserApi, UserApiDetails, FollowApi, FollowApiDetails, UserLoginAPIView

urlpatterns = [
    path('', UserApi.as_view(), name='User'),
    path('login/', UserLoginAPIView.as_view(), name='User'),
    path('<int:pk>/', UserApiDetails.as_view(), name='User'),
    path('follow/', FollowApi.as_view(), name='Follow'),
    path('<int:pk>/follow/<int:id>/', FollowApiDetails.as_view(), name='Follow'),


]
