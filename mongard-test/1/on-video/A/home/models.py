from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)