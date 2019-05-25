from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import jwt
from tasks.authentication import TaskTokenAuth

from tasks.models import TaskList, ListAccess


class ListAdd(APIView):
    authentication_classes = (TaskTokenAuth, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if request.data.get('name', None) and request.data.get('name') != '':
            # Getting request data
            name = request.data.get('name')
            description = request.data.get('description') if request.data.get('description', None) else ''

            # Writing to database
            try:
                new_list = TaskList(name=name, description=description)
                new_list.save()
                new_list_access = ListAccess(user=request.user, list=new_list, role='owner')
                new_list_access.save()

                # Response back
                res_dict = {
                    'status': 'success',
                    'message': 'List created successfully',
                    'data': {'id': new_list.id, 'name': new_list.name, 'description': new_list.description}
                }
                res = Response()
                res.status_code = 201
                res.data = res_dict

            except ValueError as val_err:
                # Response back
                res_dict = {
                    'status': 'failed',
                    'message': 'Something went wrong writing to DB, {0}'.format(val_err),
                    'data': {}
                }
                res = Response()
                res.status_code = 400
                res.data = res_dict

            except Exception as e:
                # Response back
                res_dict = {
                    'status': 'failed',
                    'message': 'Something unexpected happened!, {0}'.format(e),
                    'data': {}
                }
                res = Response()
                res.status_code = 400
                res.data = res_dict

            return res
