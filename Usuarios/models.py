from django.db import models
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

# Modelo personalizado de usuario
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('admin', 'Administrador'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

# Función para crear el usuario administrador por defecto
@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model() 
    if not User.objects.filter(username='admin').exists():
        # Crear el usuario administrador y asignarle el rol de 'admin'
        admin_user = User.objects.create_superuser(
            username='admin', 
            password='admin', 
            email='admin@example.com',
            first_name='Admin'
        )
        admin_user.role = 'admin'  # Asigna explícitamente el rol 'admin'
        admin_user.save()  # Guarda el cambio en la base de datos

        # Opcional: Asignar el grupo 'Admin'
        admin_group, created = Group.objects.get_or_create(name='Admin')
        admin_user.groups.add(admin_group)
        
@receiver(post_save, sender=CustomUser)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)