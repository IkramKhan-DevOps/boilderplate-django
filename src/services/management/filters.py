import django_filters
from django import forms

from .models import Country, State


class CountryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Country Name',
        widget=forms.TextInput(attrs={'placeholder': 'Country name'})
    )
    short_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='ISO Code',
        widget=forms.TextInput(attrs={'placeholder': 'ISO 3166-1 alpha-2'})
    )
    is_active = django_filters.BooleanFilter(
        label='Active',
        widget=forms.Select(choices=[('', 'All'), (True, 'Active'), (False, 'Inactive')])
    )
    class Meta:
        model = Country
        fields = ['name', 'short_name', 'is_active']


class StateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='State Name',
        widget=forms.TextInput(attrs={'placeholder': 'State name'})
    )
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        empty_label='All Countries',
        label='Country'
    )
    is_active = django_filters.BooleanFilter(
        label='Active',
        widget=forms.Select(choices=[('', 'All'), (True, 'Active'), (False, 'Inactive')])
    )
    class Meta:
        model = State
        fields = ['name', 'country', 'is_active']

