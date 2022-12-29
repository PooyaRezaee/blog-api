from django.db import models
from apps.account.models import User

class Article(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article')
    title = models.CharField(max_length=64)
    body = models.TextField()
    is_edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User,related_name='like')


    def __str__(self):
        return str(self.title)