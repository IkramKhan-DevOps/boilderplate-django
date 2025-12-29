from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import OperationalError, transaction
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
import time

from src.core.bll import get_list_header_stats
from src.core.forms import get_dynamic_crispy_form


class CustomPermissionMixin:
    permission_prefix = ''
    permission_action = ''

    def get_permission_name(self):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return f'{self.permission_prefix}.{self.permission_action}_{self.model._meta.model_name}'

    def check_permission(self, user):
        permission_name = self.get_permission_name()
        # print(permission_name)
        if permission_name:
            if not user.has_perm(permission_name):
                raise PermissionDenied("You do not have permission to access this.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())

        if not request.user.is_superuser:
            try:
                self.check_permission(request.user)
            except PermissionDenied:
                template = loader.get_template('403.html')
                return HttpResponse(template.render({}, request), status=403)
        # noinspection PyUnresolvedReferences
        return super().dispatch(request, *args, **kwargs)


class CoreListViewMixin(CustomPermissionMixin, ListView):
    permission_action = 'view'
    permission_prefix = None
    model = None
    form_class = None
    paginate_by = 20
    filter_class = None
    aggregation_fields = None

    def get_list_header(self, qs):
        return get_list_header_stats(qs, self.aggregation_fields)

    def get_qs(self):
        """
        Returns the queryset for the list view.
        Override this method if you need to customize the queryset.
        """
        return self.model.objects.all()

    def get_form_class(self):
        if self.form_class is not None:
            return self.form_class
        if self.model is None:
            raise ValueError("You must set the model attribute before calling get_form_class")
        return get_dynamic_crispy_form(self.model)

    def get_queryset(self):
        queryset = self.get_qs()
        if self.filter_class:
            self.filterset = self.filter_class(self.request.GET, queryset=queryset)
            return self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        # noinspection PyProtectedMember
        context = super().get_context_data(**kwargs)
        queryset_qs = self.get_queryset()

        _form_class = self.get_form_class()
        object_forms = {obj.id: _form_class(instance=obj) for obj in context['object_list']}

        context['form'] = _form_class
        context['filter_form'] = self.filterset.form if self.filter_class else None
        context['object_forms'] = object_forms
        context['model_class'] = self.model
        context['list_header'] = self.get_list_header(queryset_qs) if self.aggregation_fields else None
        context['model_verbose_name'] = self.model._meta.verbose_name.capitalize()
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural.capitalize()
        return context


class CoreDetailViewMixin(CustomPermissionMixin, DetailView):
    """
    'related_data': {
      'items': {
        'verbose_name': 'Invoice item',
        'verbose_name_plural': 'Invoice items',
        'model_class': <InvoiceItemModel>,
        'objects': <QuerySet [...InvoiceItem instances...]>,
        'update_forms': {5: <InvoiceItemForm>, 4: <InvoiceItemForm>},
        'create_form': <InvoiceItemForm>,
        'page_obj': None
      }
    }
    """
    related_object_managers = []
    permission_action = 'view'
    permission_prefix = None
    form_class = None

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            pk=self.kwargs.get('pk'),
        )

    def get_related_object_managers(self):
        return self.related_object_managers or []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # MAIN OBJECT - DETAIL
        context['model_verbose_name'] = self.model._meta.verbose_name.capitalize()
        context['model_verbose_name_plural'] = self.model._meta.verbose_name_plural.capitalize()
        context['update_form'] = self.form_class(instance=self.object) if self.form_class else None

        related_data = {}
        for manager in self.get_related_object_managers():
            related_name = manager.related_name
            objs, forms, page_obj = manager.get_objects_and_forms(self.object, self.request)

            model_meta = manager.model_class._meta

            related_data[related_name] = {
                'verbose_name': model_meta.verbose_name.capitalize(),
                'verbose_name_plural': model_meta.verbose_name_plural.capitalize(),
                'model_class': manager.get_model(),
                'objects': objs,
                'update_forms': forms,
                'create_form': manager.get_create_form(self.object),
                'page_obj': page_obj,
            }

        context['related_data'] = related_data
        return context


class CoreCreateViewMixin(CustomPermissionMixin, CreateView):
    permission_action = 'add'
    permission_prefix = None


class CoreUpdateViewMixin(CustomPermissionMixin, UpdateView):
    permission_action = 'change'
    redirect_url = None


class CoreDeleteViewMixin(CustomPermissionMixin, View):
    permission_action = 'delete'
    model = None
    redirect_url = None
    redirect_kwargs = {}

    def post(self, request, *args, **kwargs):
        """Handle DELETE request with retry logic for database locking."""
        max_retries = 3
        retry_delay = 0.1  # 100ms

        for attempt in range(max_retries):
            try:
                return self._execute_delete(request, *args, **kwargs)
            except OperationalError as e:
                if 'database is locked' in str(e) and attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    messages.error(request, "Database is temporarily unavailable. Please try again.")
                    return self._get_redirect(request, kwargs)

        messages.error(request, "Delete operation failed after multiple attempts.")
        return self._get_redirect(request, kwargs)

    @transaction.atomic
    def _execute_delete(self, request, *args, **kwargs):
        """Execute the actual delete logic within a transaction."""
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        obj.delete()
        messages.success(request, f"{self.model._meta.verbose_name} deleted successfully.")
        return self._get_redirect(request, kwargs)

    def _get_redirect(self, request, kwargs):
        """Get the redirect URL after delete."""
        redirect_url_name = request.GET.get("redirect_url")
        redirect_pk = request.GET.get("redirect_pk")

        if redirect_url_name:
            if redirect_pk:
                return redirect(reverse(redirect_url_name, kwargs={"pk": redirect_pk}))
            return redirect(reverse(redirect_url_name))

        # Default fallback
        redirect_kwargs = {k: v for k, v in kwargs.items() if k != 'pk'}
        return redirect(reverse(self.redirect_url, kwargs=redirect_kwargs or self.redirect_kwargs))