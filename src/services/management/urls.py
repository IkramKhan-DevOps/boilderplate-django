from django.urls import path, include
from .views import (

    CountryListView, CountryCreateView, CountryUpdateView, CountryDeleteView,
    StateListView, StateCreateView, StateUpdateView, StateDeleteView,

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


]