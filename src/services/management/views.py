from .filters import (
    CountryFilter, StateFilter, IndustryFilter, AnnualIncomeFilter, PlatformFilter
)
from .mixins import GenericListViewMixin, GenericDeleteViewMixin
from .models import (
    Country,
    State,
    Industry,
    AnnualIncome, Platform
)
from ...core.views import AjaxCRUDView


""" COUNTRY VIEWS """


class CountryListView(GenericListViewMixin):
    model = Country
    filter_class = CountryFilter


class CountryCreateView(AjaxCRUDView):
    model = Country


class CountryUpdateView(AjaxCRUDView):
    model = Country


class CountryDeleteView(GenericDeleteViewMixin):
    model = Country
    redirect_url = 'management:country_list'


""" STATE VIEWS """


class StateListView(GenericListViewMixin):
    model = State
    filter_class = StateFilter


class StateCreateView(AjaxCRUDView):
    model = State


class StateUpdateView(AjaxCRUDView):
    model = State


class StateDeleteView(GenericDeleteViewMixin):
    model = State
    redirect_url = 'management:state_list'


""" INDUSTRY VIEWS """


class IndustryListView(GenericListViewMixin):
    model = Industry
    filter_class = IndustryFilter


class IndustryCreateView(AjaxCRUDView):
    model = Industry


class IndustryUpdateView(AjaxCRUDView):
    model = Industry


class IndustryDeleteView(GenericDeleteViewMixin):
    model = Industry
    redirect_url = 'management:industry_list'


""" ANNUAL INCOME VIEWS """


class AnnualIncomeListView(GenericListViewMixin):
    model = AnnualIncome
    filter_class = AnnualIncomeFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # AnnualIncome_records()
        return context


class AnnualIncomeCreateView(AjaxCRUDView):
    model = AnnualIncome


class AnnualIncomeUpdateView(AjaxCRUDView):
    model = AnnualIncome


class AnnualIncomeDeleteView(GenericDeleteViewMixin):
    model = AnnualIncome
    redirect_url = 'management:annualincome_list'


""" PLATFORMS """


class PlatformListView(GenericListViewMixin):
    model = Platform
    filter_class = PlatformFilter


class PlatformCreateView(AjaxCRUDView):
    model = Platform


class PlatformUpdateView(AjaxCRUDView):
    model = Platform


class PlatformDeleteView(GenericDeleteViewMixin):
    model = Platform
    redirect_url = 'management:platform_list'