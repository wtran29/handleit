from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import jwt
from tasks.authentication import TaskTokenAuth

from tasks.models import TaskList, ListAccess

'''
POST - lists/add
1. Authenticating user
2. Reading request body params - name, description, urgency. If name and urgency not provided, response back with error msg
3. Create TaskList obj with params and save to database
4. Create ListAccess obj with User from request and Tasklist obj created and save to database
5. Response back with message and data
'''


class ListAdd(APIView):
    authentication_classes = (TaskTokenAuth, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if request.data.get('name', None) and request.data.get('name') != '':
            # Getting request data
            name = request.data.get('name')
            description = request.data.get('description') if request.data.get('description', None) else ''
            urgency = request.data.get('urgency')

            # Writing to database
            try:
                new_list = TaskList(name=name, description=description, urgency=urgency)
                new_list.save()
                new_list_access = ListAccess(user=request.user, list=new_list, role='owner')
                new_list_access.save()

                # Response back
                res_dict = {
                    'status': 'success',
                    'message': 'List created successfully',
                    'data': {'id': new_list.id, 'name': new_list.name, 'description': new_list.description, 'urgency': new_list.urgency}
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


'''
GET lists/list
1. Authenticate user
2. Get lists that belong to User in database
3. Respond back with list of Lists
'''


class ListShow(APIView):
    authentication_classes = (TaskTokenAuth, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        res_dict = {
            'status': '',
            'message': '',
            'data': None
        }

        try:
            list_ids = ListAccess.objects.values_list('list').filter(user=request.user)
            print(list_ids)
            lists = TaskList.objects.filter(id__in=list_ids).values()
            print(lists)
            res_dict['status'] = 'Success'
            res_dict['message'] = 'Retrieve list of task lists'
            res_dict['data'] = lists

        except Exception as e:
            print(e)
            res_dict['status'] = 'Failed'
            res_dict['message'] = 'Something went wrong retrieving data. Error: ' + e.__str__()
            res_dict['data'] = None

        return Response(res_dict)
    