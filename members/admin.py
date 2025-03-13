from django.contrib import admin
from .models import UserOption

# Register your models here.

@admin.register(UserOption)
class UserOptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'option')