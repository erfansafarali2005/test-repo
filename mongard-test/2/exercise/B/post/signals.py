from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post

@receiver(post_save , sender=Post)
def create_post(sender , **kwargs):
    if kwargs['created']:
        print(f'a new post created {kwargs["instance"]}')