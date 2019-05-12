from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.conf import settings


class Register(APIView):
    def post(self, request, *args, **kwargs):
        required_fields = ['username', 'password', 'email']
        try:
            data = request.data
            # use all() to check if all fields are present in data
            if all(key in data for key in required_fields):
                try:
                    username = self.validate_required_input(required_fields[0], data[required_fields[0]])
                    password = self.validate_required_input(required_fields[1], data[required_fields[1]])
                    email = self.validate_required_input(required_fields[2], data[required_fields[2]])
                except ValidationError as error:
                    return Response({"error": str(error.messages[0])}, status=status.HTTP_400_BAD_REQUEST)

                # Create user object
                new_user = User()
                new_user.username = username
                new_user.password = make_password(password)
                new_user.email = email

                # Setting/checking for additional params
                try:
                    new_user.firstname = data['firstname'] if data['firstname'] is not None else
                except KeyError:
                    print("Error checking first name")
                try:
                    new_user.lastname = data['lastname'] if data['lastname'] is not None else
                except KeyError:
                    print("Error checking last name")

                new_user.save()

                return Response({"status": "Success"}, status=status.HTTP_201_CREATED)

            else:
                return Response({"error": "Required field(s) needed. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected error occurred: " + str(e))
            return Response({"error": "Unexpected error occurred, please notify admin."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        