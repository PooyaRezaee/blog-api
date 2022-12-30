from rest_framework import serializers
from .models import Article

class ArticlesSerializer(serializers.ModelSerializer):
    count_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ('modified','like','body')
    
    def get_count_like(self,obj):
        return obj.like.count()

class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','body')

    def create_article(self,validated_data,user):
        Article.objects.create(
            author=user,
            title=validated_data['title'],
            body=validated_data['body'],
        )