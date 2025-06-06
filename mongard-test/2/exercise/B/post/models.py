from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts') # user.posts
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)


    def get_absolute_url(self):
        return reverse("post:post_detail" , args=(self.id , self.slug))



class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomments' ) #user.ucomments
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='pcomments') #post.pcomments
    reply = models.ForeignKey('self' , on_delete=models.CASCADE , related_name='rcomments' , blank=True , null=True) # may we don't have any replies
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) #updating comment details

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'