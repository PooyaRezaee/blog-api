from django.urls import path
from .views import *

urlpatterns = [
    path("users/", UsersApiView.as_view())
]