import jwt
from django.conf import settings
from rest_framework import exceptions, permissions
from rest_framework.authentication import (
    get_authorization_header)
from django.utils.translation import get_language
from users.models import User


class TokenAuthentication(permissions.BasePermission):
    model = None

    def get_model(self):
        return User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            email = payload['email']
            userid = payload['id']

            user = model.objects.get(
                email=email,
                id=userid,
            )

            if not user.auth_token == bytes.decode(token):
                msg = {'message_en': "Token mismatch.",
                       "message_ar": "رمز غير متطابق."}
                raise exceptions.AuthenticationFailed(msg)

        except (jwt.ExpiredSignature, jwt.DecodeError,
                jwt.InvalidTokenError, jwt.InvalidSignatureError) as e:
            msg = {"message_en": "Invalid Token.",
                   "message_ar": "رمز دخول خاطئ.",
                   "status": False}
            raise exceptions.AuthenticationFailed(msg)

        except User.DoesNotExist:
            msg = {"message_en": "User phone dose not exist.",
                   "message_ar": "هذا المستخدم غير موجود."}
            raise exceptions.AuthenticationFailed(msg)

        # check if user change his language allover our applications
        # lang = get_language()
        # if user.language != lang:
        #     user.language = lang
        #     user.save()

        return user, token,

    def authenticate_header(self, request):
        return 'Token'