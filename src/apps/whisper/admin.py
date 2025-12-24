# DONE : VERIFIED
from django.contrib import admin

from src.apps.whisper.models import EmailNotification


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'created_at')
