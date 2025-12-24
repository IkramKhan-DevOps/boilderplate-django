from django.contrib import admin

from .models import (
   Application
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'tagline', 'is_active', 'created_on')

