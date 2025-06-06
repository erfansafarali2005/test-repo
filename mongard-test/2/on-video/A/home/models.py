from django.db import models
from django.contrib.auth.models import User
from django.template.context_processors import request
from django.urls import reverse

class Post(models.Model) :
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.slug} + {self.created}'

    def get_absolute_url(self):
        return reverse('home:post_detail' , args=(self.id , self.slug)) # {{ post.get_absolute_url }}


class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomments')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self' , on_delete=models.CASCADE , related_name='rcomments' , blank=True , null=True)
    #                                                                                             ^-> maybe we don't have any comment
    def __str__(self):
        return f'{self.user} commentd {self.body[:30]}'