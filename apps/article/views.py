from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Article
from .serializers import ArticlesSerializr

class ArticlesApiView(ListAPIView):
    serializer_class = ArticlesSerializr
    queryset = Article.objects.all()