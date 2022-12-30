from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .models import Article
from .serializers import ArticlesSerializer,CreateArticleSerializer

__all__ = [
    'ArticlesApiView',
    'ArticleCreateApiView',
]

class ArticlesApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticlesSerializer
    queryset = Article.objects.all()

class ArticleCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateArticleSerializer
    throttle_scope = 'create_article'

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_article(serializer.data,self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)