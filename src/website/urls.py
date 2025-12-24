from django.urls import path

from .views import (
    HomeView
)

app_name = "website"
urlpatterns = [
    # path('', HomeView.as_view(), name='home')
]
