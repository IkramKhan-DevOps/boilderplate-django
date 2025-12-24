from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404,  HttpResponse
from django.shortcuts import redirect
from django.template import loader

from src.core.mixins import (CoreListViewMixin, CoreDetailViewMixin, CoreCreateViewMixin,
    CoreUpdateViewMixin, CoreDeleteViewMixin)
from src.services.accounts.models import UserType

""" ROLES MIXINS --------------------------------------------------------------------------------------------------- """


class SuperUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class StaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class StaffOrClientRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and (
                user.is_staff or
                user.is_superuser or
                user.user_type == UserType.client
            )
        )

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")


class ClientMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return redirect('dashboard:dashboard')

        company = user.get_company()
        if not company:
            return redirect('onboarding:cross_verification')

        if not company.complete_full:
            return redirect('onboarding:cross_verification')

        return super().dispatch(request, *args, **kwargs)



class GenericListViewMixin(CoreListViewMixin):
    permission_prefix = 'accounts'


class GenericDetailViewMixin(CoreDetailViewMixin):
    permission_prefix = 'accounts'


class GenericCreateViewMixin(CoreCreateViewMixin):
    permission_prefix = 'accounts'


class GenericUpdateViewMixin(CoreUpdateViewMixin):
    permission_prefix = 'accounts'


class GenericDeleteViewMixin(CoreDeleteViewMixin):
    permission_prefix = 'accounts'





