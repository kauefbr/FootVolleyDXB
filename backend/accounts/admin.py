from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo', 'first_name', 'last_name')
    list_filter = ('tipo', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')