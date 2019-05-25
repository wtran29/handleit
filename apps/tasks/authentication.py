from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User
from django.utils.six import text_type
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
import jwt


class TaskTokenAuth(authentication.BaseAuthentication):
    def authenticate(self, request):

        # Getting token from request header
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        print(auth)
        if isinstance(auth, text_type):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)

        auth = auth.split()

        if not auth or auth[0].lower() != 'bearer'.encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        # Token validation
        try:
            decoded_token_payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.exceptions.InvalidSignatureError:
            return exceptions.AuthenticationFailed("Invalid Signature, token compromised.")
        except jwt.exceptions.ExpiredSignatureError:
            return exceptions.AuthenticationFailed("Token expired.")
        except (jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError):
            return exceptions.AuthenticationFailed("Invalid Token")

        # Checking token type
        if not decoded_token_payload['type'] or decoded_token_payload['type'] != 'access':
            return None

        user = None
        try:
            global user
            user = User.objects.get(username=decoded_token_payload['username'])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed("User doesn't exist")
        except MultipleObjectsReturned:
            raise exceptions.AuthenticationFailed("Multiple users found")

        return user, None
