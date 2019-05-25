from django.urls import path
from django.conf.urls import url

from api.tasks.views import ListAdd, ListShow


app_name = 'tasks-api'

urlpatterns = [
    url(r'lists/add/', ListAdd.as_view()),
    url('r^lists/list', ListShow.as_view())
]