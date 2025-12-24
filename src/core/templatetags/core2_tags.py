
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def base_url():
    """
    Returns the base URL from settings
    Usage: {% base_url %}
    """
    return getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')

@register.simple_tag
def api_base_url():
    """
    Returns the API base URL
    Usage: {% api_base_url %}
    """
    base = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
    return f"{base.rstrip('/')}"