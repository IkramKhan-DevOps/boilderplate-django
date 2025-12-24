from django.urls import path, include
from .views import (

    CountryListView, CountryCreateView, CountryUpdateView, CountryDeleteView,
    StateListView, StateCreateView, StateUpdateView, StateDeleteView,
    IndustryListView, IndustryCreateView, IndustryUpdateView, IndustryDeleteView,
    AnnualIncomeListView, AnnualIncomeCreateView, AnnualIncomeUpdateView, AnnualIncomeDeleteView,
    PlatformListView, PlatformCreateView, PlatformUpdateView, PlatformDeleteView,

)

app_name = 'management'
urlpatterns = [

    path('countries/', CountryListView.as_view(), name='country_list'),
    path('countries/create/', CountryCreateView.as_view(), name='country_create'),
    path('countries/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('countries/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),

    path('states/', StateListView.as_view(), name='state_list'),
    path('states/create/', StateCreateView.as_view(), name='state_create'),
    path('states/update/<int:pk>/', StateUpdateView.as_view(), name='state_update'),
    path('states/delete/<int:pk>/', StateDeleteView.as_view(), name='state_delete'),

    path('industries/', IndustryListView.as_view(), name='industry_list'),
    path('industries/create/', IndustryCreateView.as_view(), name='industry_create'),
    path('industries/update/<int:pk>/', IndustryUpdateView.as_view(), name='industry_update'),
    path('industries/delete/<int:pk>/', IndustryDeleteView.as_view(), name='industry_delete'),

    path('annual-income/', AnnualIncomeListView.as_view(), name='annualincome_list'),
    path('annual-income/create/', AnnualIncomeCreateView.as_view(), name='annualincome_create'),
    path('annual-income/update/<int:pk>/', AnnualIncomeUpdateView.as_view(), name='annualincome_update'),
    path('annual-income/delete/<int:pk>/', AnnualIncomeDeleteView.as_view(), name='annualincome_delete'),

    path('platforms/', PlatformListView.as_view(), name='platform_list'),
    path('platforms/create/', PlatformCreateView.as_view(), name='platform_create'),
    path('platforms/update/<int:pk>/', PlatformUpdateView.as_view(), name='platform_update'),
    path('platforms/delete/<int:pk>/', PlatformDeleteView.as_view(), name='platform_delete'),

]

# API ENDPOINTS
urlpatterns += [
    path('api/', include('src.services.management.api.urls')),
]
