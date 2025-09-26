from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'first_name', 'last_name', 'email', 'username']
    list_display = ('id', 'first_name', 'last_name', 'username')

admin.site.register(User, UserAdmin)
