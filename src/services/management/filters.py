import django_filters
from django import forms

from .models import Country, State, Industry, AnnualIncome, Platform


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


class IndustryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Industry Name',
        widget=forms.TextInput(attrs={'placeholder': 'Industry name'})
    )
    is_active = django_filters.BooleanFilter(
        label='Active',
        widget=forms.Select(choices=[('', 'All'), (True, 'Active'), (False, 'Inactive')])
    )
    class Meta:
        model = Industry
        fields = ['name', 'is_active']


class AnnualIncomeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Tax Name',
        widget=forms.TextInput(attrs={'placeholder': 'Tax name'})
    )
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        empty_label='All States',
        label='State'
    )
    industry = django_filters.ModelChoiceFilter(
        queryset=Industry.objects.all(),
        empty_label='All Industries',
        label='Industry'
    )
    is_active = django_filters.BooleanFilter(
        label='Active',
        widget=forms.Select(choices=[('', 'All'), (True, 'Active'), (False, 'Inactive')])
    )
    class Meta:
        model = AnnualIncome
        fields = ['name', 'state', 'is_active']


class PlatformFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'name'})
    )
    domain = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Domain',
        widget=forms.TextInput(attrs={'placeholder': 'domain'})
    )
    protocol = django_filters.BooleanFilter(
        label='Protocol',
        widget=forms.Select(choices=[('', 'All'), ('http', 'HTTP'), ('https', 'HTTPS')])
    )
    class Meta:
        model = Platform
        fields = ['name', 'domain', 'protocol']
