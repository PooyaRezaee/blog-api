from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ('title','author','created')
    list_filter = ('created','title','author')
    search_fields = ('title','body')
    ordering = ('created',)
    exclude = ('like',)