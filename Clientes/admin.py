from django.contrib import admin
from .models import Cliente, ClienteEliminado


admin.site.register(Cliente)
admin.site.register(ClienteEliminado)