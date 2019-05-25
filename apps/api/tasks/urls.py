from django.urls import path
from django.conf.urls import url

from api.tasks.views import ListAdd, ListShow, TaskAdd, TaskShow


app_name = 'tasks-api'

urlpatterns = [
    url(r'lists/add(?:\/)?$', ListAdd.as_view()),
    url(r'^lists/list(?:\/)?$', ListShow.as_view()),
    url(r'^tasks/add(?:\/)?$', TaskAdd.as_view()),
    url(r'^tasks/list$', TaskShow.as_view())
]