from datetime import datetime
from django.core.exceptions import FieldError
from django.db.models import Sum

from .models import Application


def get_or_create_application():
    applications = Application.objects.all()
    return applications[0] if applications else Application.objects.create()


def get_action_urls(instance, user, include_create=False):
    """
    Returns action URLs (update, delete, detail) dynamically
    based on instance metadata and allowed actions declared on the model.
    """
    model_meta = instance._meta
    app_label = model_meta.app_label
    model_name = model_meta.model_name

    # Get allowed actions with safe default
    allowed_actions = getattr(instance, "allowed_actions", [])
    if not allowed_actions:
        allowed_actions = ["update", "delete", "detail"]

    route_base = f"{app_label}:{model_name}"
    action_urls = {}

    action_permission_map = {
        "update": f"{app_label}.change_{model_name}",
        "delete": f"{app_label}.delete_{model_name}",
        "detail": f"{app_label}.view_{model_name}",
        "list": f"{app_label}.view_{model_name}",
    }

    for action in allowed_actions:
        if action in action_permission_map and (user.has_perm(action_permission_map[action])):
            action_urls[action] = f"{route_base}_{action}"

    if include_create and (user.has_perm(f"{app_label}.add_{model_name}")):
        action_urls["create"] = f"{route_base}_create"

    return action_urls


def get_list_header_stats(qs, fields):
    queryset = qs
    stats = {
        'total_count': queryset.count(),
        'this_month_count': queryset.filter(created_at__month=datetime.now().month).count(),
    }
    try:
        active_count = queryset.filter(is_active=True).count()
        stats['active_count'] = active_count
        stats['inactive_count'] = stats['total_count'] - active_count
    except FieldError:
        pass
    field_stats = {}
    for field in fields:
        try:
            result = queryset.aggregate(total=Sum(field))['total'] or 0
            field_stats[field] = result
        except FieldError:
            continue
    stats['fields'] = field_stats
    return stats
