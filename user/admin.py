from django.contrib import admin
from .models import User, Registro

class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'first_name', 'last_name', 'email', 'username']
    list_display = ('id', 'first_name', 'last_name', 'username')

class RegistroAdmin(admin.ModelAdmin):
    search_fields = ['id', 'accion', 'modelo', 'descripcion', 'fecha']
    list_display = ('id', 'accion', 'modelo', 'descripcion', 'fecha')

admin.site.register(User, UserAdmin)
admin.site.register(Registro, RegistroAdmin)
