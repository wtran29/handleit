from django.contrib import admin
from django.urls import path

from .views import Register

app_name = 'users-api'

urlpatterns = [
    path('register/', Register.as_view())
]