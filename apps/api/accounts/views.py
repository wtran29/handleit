from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.conf import settings


# Could have import CreateAPIView from rest_framework.generics
class Register(APIView):
    def post(self, request, *args, **kwargs):
        required_fields = ['username', 'password', 'email']
        try:
            data = request.data
            # use all() to check if all fields are present in data
            if all(key in data for key in required_fields):
                try:
                    username = self.validate(required_fields[0], data[required_fields[0]])
                    password = self.validate(required_fields[1], data[required_fields[1]])
                    email = self.validate(required_fields[2], data[required_fields[2]])
                except ValidationError as error:
                    return Response({"error": str(error.messages[0])}, status=status.HTTP_400_BAD_REQUEST)

                # Create user object
                new_user = User()
                new_user.username = username
                new_user.password = make_password(password)
                new_user.email = email

                # Setting/checking for additional params
                try:
                    new_user.firstname = data['firstname'] if data['firstname'] is not None else ""
                except KeyError:
                    print("Error checking first name")
                try:
                    new_user.lastname = data['lastname'] if data['lastname'] is not None else ""
                except KeyError:
                    print("Error checking last name")

                new_user.save()

                return Response({"status": "Success"}, status=status.HTTP_201_CREATED)

            else:
                return Response({"error": "Required field(s) needed. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected error occurred: " + str(e))
            return Response({"error": "Unexpected error occurred, please notify admin."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def validate(field, data):
        username = data['username']
        password = data['password']
        email = data['email']

        if field == 'username':
            if username is not None and type(username) == str and len(username) > 0:
                if User.objects.filter(username=username).exists():
                    raise ValidationError("This user is already registered.")
                return data
            else:
                raise ValidationError("Invalid username. This field must be filled.")

        elif field == 'password':
            if password is not None and type(password) == str and len(password) >= 8:
                return data
            else:
                raise ValidationError("Invalid password. Must be at least 8 characters long.")

        elif field == 'email':
            if email is not None and type(email) == str and len(email) > 0:
                try:
                    validate_email(email)
                except ValidationError:
                    raise ValidationError("Invalid email. Please try again.")
                else:
                    if User.objects.filter(email=email).exists():
                        raise ValidationError("Email already exists. Please try logging in.")
                    return data
            else:
                raise ValidationError("Invalid email. Please try again.")

        else:
            raise ValidationError("Invalid data being passed.")


class Login(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Authentication Successful")
