from rest_framework import serializers
from .models import Article

class ArticlesSerializr(serializers.ModelSerializer):
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('modified','like')
    
    def get_count_like(self,obj):
        return obj.like.count()
