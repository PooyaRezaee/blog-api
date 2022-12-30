from django.urls import path
from rest_framework.authtoken import views as auth_view
from .views import *

urlpatterns = [
    path("users/", UserListApiView.as_view()),
    path("users_full/", FullUserListApiView.as_view()),
    path("user/", UserApiView.as_view()),
    path("user/<int:pk>/", UserDetailAPiView.as_view()),
    path("user/delete/<int:pk>/", DeleteUserApiView.as_view()),
    path("user/register/", UserCreateView.as_view()),
    path("user/token/", auth_view.ObtainAuthToken.as_view()),
    path("user/token/refresh/", ChangeToken.as_view()),
]

"""
    Urls Help
    
    root-url => /account/

    For Any
        - Register         => register/              -> POST
        - Get Toke         => token/                 -> POST
        - Refresh Token    => token/refresh/         -> POST
        - Information User => user/                  -> Get           --> Need Athenticate
        - List Users       => users/                 -> Get
        - Update Info Self => user/<self_id>/        -> GET.PUT.PATCH --> Need Athenticate
        - Delete Self      => user/delete/<self_id>/ -> DELETE        --> Need Athenticate
    
    For Admin -> Need Athenticate
        - List FullDetail Users   => users_full/       -> GET
        - Detail And Update User  => user/<id>/        -> GET,PUT.PATCH
        - Delete User             => user/delete/<id>/ -> DELETE

"""