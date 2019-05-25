from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import jwt
from tasks.authentication import TaskTokenAuth


class ListAdd(APIView):
    authentication_classes = (TaskTokenAuth, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if request.data.get('name', None) and request.data.get('name') != '':
            # Getting request data
            name = request.data.get('name')
