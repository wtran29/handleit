from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import jwt
from tasks.authentication import TaskTokenAuth

from tasks.models import TaskList, ListAccess, Task

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


'''
POST tasks/add
1. Authenticate user
2. Read request body params with additional params list
3. Check if list exists with id and current user is owner of list
'''


class TaskAdd(APIView):
    authentication_classes = (TaskTokenAuth, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        res_dict = {
            'status': None,
            'message': None,
            'data': None
        }

        req_list_id = request.data.get('list_id')
        req_task_name = request.data.get('name')
        req_task_desc = request.data.get('description') if request.data.get('description', None) else ''
        req_task_urg = request.data.get('urgency')

        if req_list_id and TaskList.objects.filter(id=req_list_id).exists() and req_task_name and req_task_name != '' and req_task_urg and req_task_urg != '':
            try:
                task_list = TaskList.objects.get(id=req_list_id)
                user_has_perm = ListAccess.objects.filter(user=request.user, list=task_list)

                if user_has_perm.count() != 1 or user_has_perm.first().role != 'owner':
                    raise PermissionError("You do not have permission to edit this list")

                new_task = Task(name=req_task_name, list=task_list, description=req_task_desc, urgency=req_task_urg)
                new_task.save()

                res_dict['status'] = 'success'
                res_dict['message'] = 'Task created!'
                res_dict['data'] = {
                    'name': new_task.name,
                    'description': new_task.description,
                    'urgency': new_task.urgency,
                    'task_completed': new_task.task_completed,
                    'list_id': new_task.list.id
                }

                res = Response(res_dict)
                res.status_code = 200

            except PermissionError as perm_err:
                res_dict['status'] = 'failed'
                res_dict['message'] = 'Permission denied! Error: ' + perm_err.__str__()
                res_dict['data'] = None
                res = Response(res_dict)
                res.status_code = 403

            except Exception as e:
                res_dict['status'] = 'failed'
                res_dict['message'] = 'Something went wrong, Error: ' + e.__str__()
                res_dict['data'] = None
                res = Response(res_dict)
                res.status_code = 500

        else:
            res_dict['status'] = 'failed'
            res_dict['message'] = 'Invalid name or list_id passed.'
            res_dict['data'] = None
            res = Response(res_dict)
            res.status_code = 400

        return res

