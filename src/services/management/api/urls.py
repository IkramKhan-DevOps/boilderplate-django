from django.urls import path

from .views import (
    AnnualIncomeFilterAPIView,
)


urlpatterns = [
    path(
        'annual-income/state/<int:state_id>/industry/<int:industry_id>/',
        AnnualIncomeFilterAPIView.as_view(),
        name='annual_income_filter_api'
    ),
]