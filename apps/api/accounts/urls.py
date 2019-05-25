from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from .views import Register, Login, LoginRefresh

app_name = 'users-api'

urlpatterns = [
    path('register/', Register.as_view()),
    url(r'^login(?:\/)?$', Login.as_view()),
    url('r^login/refresh(?:\/)?$', LoginRefresh.as_view()),
]