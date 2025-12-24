from django.contrib import admin

from .models import (
    Country, State
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'language', 'currency', 'phone_code', 'is_active', 'created_on')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'is_active', 'created_on')
    search_fields = ('name', 'country__name')
    list_filter = ('is_active',)
    ordering = ('-created_on',)