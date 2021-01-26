from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users.api.serializers import UserSerializer, FollowSerializer
from users.models import User, Follow


class UserApi(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", }, status=201)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)


class UserApiDetails(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        serializer = UserSerializer(user)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=200)

    def put(self, request, *args, **kwargs):
        data = request.data
        user = get_object_or_404(User, id=kwargs["pk"])
        if request.user.user_name != user.user_name:
            raise PermissionDenied
        serializer = UserSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        if request.user.auth_token != user.auth_token:
            raise PermissionDenied
        user.delete()
        return Response({"message": "Done", "status": True}, status=200)


class FollowApi(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, *args, **kwargs):
        queryset = Follow.objects.all()
        serializer = FollowSerializer(queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", }, status=201)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=201)
        return Response({"message": serializer.errors, "status": True}, status=201)


class FollowApiDetails(generics.RetrieveUpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    # def retrieve(self, request, *args, **kwargs):
    #     user = get_object_or_404(User, id=kwargs["pk"])
    #     serializer = FollowSerializer(user)
    #     return Response({"result": serializer.data, "message": "Done", "status": True}, status=200)

    def delete(self, request, *args, **kwargs):
        follow = get_object_or_404(User, id=kwargs["id"])
        if request.user != follow.user_name:
            raise PermissionDenied
        follow.delete()

        follow = Follow.objects.filter(user_id=kwargs["pk"], follow_id=kwargs["id"]).delete()
        return Response({"message": "Done", "status": True}, status=200)
