from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from src.core.bll import get_action_urls

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('sent', 'Sent'),
    ('failed', 'Failed'),
    ('retry', 'Retry'),
]


class EmailNotification(models.Model):
    allowed_actions = ["list"]

    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipient = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    failed_attempts = models.PositiveIntegerField(default=0)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)  # New field

    # Generic foreign key to relate this model to any other model
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    object_id = models.CharField(max_length=36)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Email to {self.recipient} at {self.updated_at if self.updated_at else 'Not Sent'}"

    @property
    def get_display_fields(self):
        """Return fields that should be displayed in the template."""
        return ['subject', 'recipient', 'status', 'failed_attempts', 'created_at']

    def get_action_urls(self, user):
        return get_action_urls(self, user)
