from django.urls import path
from .views import *

urlpatterns = [
    path("", ArticlesApiView.as_view()),
    path("create/", ArticleCreateApiView.as_view()),
    path("<int:pk>/", DetailArticleApiView.as_view()),
    path("delete/<int:pk>/", DeleteArticleApiView.as_view()),
    path("like/", LikeArticleApiView.as_view()),
    path("dislike/", DislikeArticleApiView.as_view()),
]


"""
    Urls Help

    root-url => /article/

    For Any
        - List All Articles              => /               -> GET
        - Create New Article             => create/         -> POST  --> Need Athenticate
        - Detail Or Update Self Article  => <id>/           -> GET,PUT,PATCH --> Need Athenticate for update
        - Delete Article                 => delete/<id>/    -> Delete --> Need Athenticate
        - Like Article                   => like/           -> POST --> Need Athenticate
        - DisLike Article                => dislike/        -> POST --> Need Athenticate

"""