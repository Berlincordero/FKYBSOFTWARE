from django.db import models



# Create your models here.

from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')