from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User

# @receiver(post_save, sender=User)
# def create_user(sender,instance , created, **kwargs):
#     if sender.is_superuser:
#         if created:
#             Profile.objects.create(user=instance)
