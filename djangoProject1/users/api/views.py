import string
import jwt
from django.core.cache import cache
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from djangoProject1 import settings
from users.api.serializers import UserSerializer, FollowSerializer
from users.models import User, Follow
import random


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


def code_generator(size=5, chars=string.digits):
    code = ''.join(random.choice(chars) for _ in range(size))
    if code[0] == '0':
        code = code.replace('0', random.choice(
            string.digits.replace('0', '')), 1)
    return code


class UserLoginAPIView(APIView):
    login_code = "حي الله من جانا، رمز التفعيل هو %s"

    def get(self, request, *args, **kwargs):
        # Insure pass phone number
        user_phone = request.GET.get('user_phone', None)
        if user_phone is None:
            return Response({
                "message": "Invalid parameters.",
                "status": False
            }, status=404)

        # Gets two format of saudi phone numbers

        try:
            user = User.objects.get(
                user_phone=user_phone
            )
            # user.auth_token = None
            # user.save()طب هفكس مشكلة ع

            # Generate a 5 digits login cod
            code = code_generator()

            # Puts generated code into redis  for 180s
            cache.set(
                '{0}-verification'.format(user_phone),
                code,
                timeout=180
            )

            result = {
                "message_en": "A verification code has been sent to you.",
                "message_ar": "تم ارسال كود التحقق الي هاتفكم.",
                "status": True, "code": code
            }

            return Response(result, status=201)
        except User.DoesNotExist:
            # create new user and profile
            serializer = UserSerializer(data={"user_phone": user_phone})
            if serializer.is_valid():
                user = serializer.save()
                code = code_generator()

                # Puts generated code into redis  for 180s
                cache.set(
                    '{0}-verification'.format(user_phone),
                    code,
                    timeout=180
                )

                result = {
                    "message_en": "A verification code has been sent to you.",
                    "message_ar": "تم ارسال كود التحقق الي هاتفكم.",
                    "status": True, "code": code}

                return Response(result, status=201)

            return Response({
                "result": serializer.errors,
                "message_en": "Please, fill the data correctly.",
                "message_ar": "من فضلك املأ البيانات بشكل صحيح",
                "status": False
            }, status=422)

    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        user_phone = request.data.get('user_phone', None)

        cached_value = '{0}-verification'.format(user_phone)

        try:
            user = User.objects.get(
                user_phone=user_phone
            )

            if cached_value in cache:
                value = cache.get(cached_value)
                if value == code:
                    auth_token = user.auth_token
                    if auth_token is None:
                        payload = {
                            'id': user.id,
                            'user_phone': user.user_phone
                        }
                        auth_token = {'token': jwt.encode(payload, settings.SECRET_KEY)}
                        user.auth_token = bytes.decode(auth_token['token'])
                        user.save()
                    serializer = UserSerializer(user)
                    return Response({
                        "result": serializer.data,
                        "status": True
                    }, status=200)
            return Response({
                "message_en": "Invalid Code.",
                "message_ar": "كود خاطئ.",
                "status": False
            }, status=422)
        except User.DoesNotExist:
            return Response({
                "message_en": "User phone dose not exist.",
                "message_ar": "هذا المستخدم غير موجود.",
                "status": False
            }, status=404)


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
