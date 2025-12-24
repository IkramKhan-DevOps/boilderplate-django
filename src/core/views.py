from json import loads
import time

from django.db import transaction, OperationalError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from src.core.forms import get_dynamic_crispy_form


class AjaxCRUDView(View):
    model = None
    form_class = None
    redirect_url = None
    redirect_kwargs = None

    def get_form_class(self):
        if self.form_class:
            return self.form_class

        if self.model is None:
            raise ValueError("You must set the model or form_class attribute.")

        return get_dynamic_crispy_form(self.model)

    def get_object(self):
        if 'pk' not in self.kwargs:
            return None
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_redirect_url(self, instance):
        if self.redirect_url:
            kwargs = self.redirect_kwargs or {}
            kwargs.setdefault('pk', instance.pk)
            return reverse(self.redirect_url, kwargs=kwargs)
        return None

    def post_additional_data(self, instance):
        """Hook to modify the instance before saving."""
        pass

    def post(self, request, *args, **kwargs):
        """Handle POST request with retry logic for database locking."""
        max_retries = 3
        retry_delay = 0.1  # 100ms

        for attempt in range(max_retries):
            try:
                return self._execute_post(request, *args, **kwargs)
            except OperationalError as e:
                if 'database is locked' in str(e) and attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Database is temporarily unavailable. Please try again.',
                    }, status=503)

        return JsonResponse({
            'status': 'error',
            'message': 'Request failed after multiple attempts.',
        }, status=503)

    @transaction.atomic
    def _execute_post(self, request, *args, **kwargs):
        """Execute the actual POST logic within a transaction."""
        obj = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            instance = form.save(commit=False)
            self.post_additional_data(instance)
            instance.save()
            form.save_m2m()
            return self.handle_success(instance)
        return self.handle_error(form)

    def handle_success(self, instance):
        redirect_url = self.get_redirect_url(instance)
        return JsonResponse({
            'status': 'success',
            'message': f'{self.model.__name__} saved successfully',
            'id': instance.pk,
            'redirect_url': redirect_url,
        })

    def handle_error(self, form):
        return JsonResponse({
            'status': 'error',
            'error_list': loads(form.errors.as_json()),
            'message': 'Form validation failed',
        }, status=400)