from .filters import (
    CountryFilter, StateFilter
)
from .mixins import GenericListViewMixin, GenericDeleteViewMixin
from .models import (
    Country,
    State,
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
