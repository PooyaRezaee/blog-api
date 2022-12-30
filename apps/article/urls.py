from django.urls import path
from .views import *

urlpatterns = [
    path("", ArticlesApiView.as_view()),
    path("create/", ArticleCreateApiView.as_view()),
]


"""
    Urls Help

    root-url => /article/

    For Any
        - List All Articles    => /        -> GET
        - Create New Article   => create/  -> POST  --> Need Athenticate

"""