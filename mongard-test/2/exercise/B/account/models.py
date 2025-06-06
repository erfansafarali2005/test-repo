from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='follower')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} to {self.to_user} | last : {self.updated}'