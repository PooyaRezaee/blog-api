from django.urls import path
from .views import *

urlpatterns = [
    path("list/", ArticlesApiView.as_view(), name="")
]
