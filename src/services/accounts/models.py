from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

from src.core.bll import get_action_urls
from src.core.models import phone_number_null_or_validator


class UserType(models.TextChoices):
    administration = 'administration', 'Administration'
    client = 'client', 'Client'


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(
        max_length=14, blank=True, null=True,
        validators=[phone_number_null_or_validator]
    )
    user_type = models.CharField(max_length=50, choices=UserType.choices, default=UserType.client)
    description = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    allowed_actions = ['delete', 'detail', 'list']

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"

        if self.username:
            return self.username

        return self.email

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)

    def get_display_fields(self):
        return ['id', 'first_name', 'last_name', 'email', 'platform', 'user_type', 'is_active', 'is_staff']

    def get_action_urls(self, user):
        return get_action_urls(self, user, True)

    def save(self, *args, **kwargs):
        self.clean()

        if self.is_staff or self.is_superuser and not self.user_type:
            self.user_type = UserType.administration

        super().save(*args, **kwargs)
