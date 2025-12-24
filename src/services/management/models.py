from email.policy import default

from django.db import models
from django.core.exceptions import ValidationError

import re
from src.core.bll import get_action_urls

""" MODELS """


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=2, unique=True, help_text='ISO 3166-1 alpha-2')
    language = models.CharField(max_length=3, default='en', help_text='ISO 639-1', null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD', help_text='ISO 4217', null=True, blank=True)
    phone_code = models.CharField(max_length=4, default='+1', help_text='e.g. +1', null=True, blank=True)

    is_services_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    allowed_actions = ['delete', 'update', ]

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def get_display_fields(self):
        return ['name', 'short_name', 'language', 'currency', 'phone_code', 'is_active']

    def get_action_urls(self, user):
        return get_action_urls(self, user, True)


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='states')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    allowed_actions = ['delete', 'update', ]

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'States'

    def __str__(self):
        return f"{self.name}"

    def get_display_fields(self):
        return ['name', 'country', 'is_active']

    def get_action_urls(self, user):
        return get_action_urls(self, user, True)