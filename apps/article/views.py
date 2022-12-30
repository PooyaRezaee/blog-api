from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateAPIView,DestroyAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .models import Article
from .serializers import ArticlesSerializer,CreateArticleSerializer,DetailArticlesSerializer
from core.permissions import IsOwerArticleOrReadOnly,IsOwerArticle

__all__ = [
    'ArticlesApiView',
    'ArticleCreateApiView',
    'DetailArticleApiView',
    'DeleteArticleApiView',
    'LikeArticleApiView',
    'DislikeArticleApiView',
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

class DetailArticleApiView(RetrieveUpdateAPIView):
    permission_classes = [IsOwerArticleOrReadOnly]
    serializer_class = DetailArticlesSerializer
    queryset = Article.objects.all()

class DeleteArticleApiView(DestroyAPIView):
    permission_classes = [IsOwerArticle]
    queryset = Article.objects.all()

class LikeArticleApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            pk = request.data['id']
        except:
            return Response({'msg':'You Must Send id Article'},status=status.HTTP_400_BAD_REQUEST)
        article = get_object_or_404(Article,pk=pk)
        if article.like.filter(pk=request.user.pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        article.like.add(request.user)
        return Response(status=status.HTTP_200_OK)

class DislikeArticleApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            pk = request.data['id']
        except:
            return Response({'msg':'You Must Send id Article'},status=status.HTTP_400_BAD_REQUEST)
        article = get_object_or_404(Article,pk=pk)
        if article.like.filter(pk=request.user.pk).exists():
            article.like.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)