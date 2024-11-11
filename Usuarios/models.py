from django.db import models
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('admin', 'Administrador'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model() 
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin', 
            password='admin', 
            email='admin@example.com',
            first_name='Admin'
        )
        admin_user.role = 'admin'  
        admin_user.save()  

        admin_group, created = Group.objects.get_or_create(name='Admin')
        admin_user.groups.add(admin_group)
        
@receiver(post_save, sender=CustomUser)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)