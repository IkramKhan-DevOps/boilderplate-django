import json
from datetime import datetime
from django import template
from django.urls import reverse
from urllib.parse import urlencode
import re

from root.settings import BASE_URL
from src.core.bll import get_action_urls
register = template.Library()


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, "")
    return ""

@register.filter
def is_bad_value(value):
    """
    Returns True if the value is considered 'bad': nan, None, empty string, or 0.
    """
    # Handles string "nan", None, empty string, and string/integer zero
    if value is None:
        return True
    value_str = str(value).strip().lower()
    if value_str == "nan" or value_str == "" or value_str == "0" or value == 0:
        return True
    return False


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def get_item(dictionary, key, related_object=None):
    if related_object:
        dictionary = dictionary[related_object]
    return dictionary.get(key)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('include/modal_create_form.html')
def model_form_create(action_url, form, model_class):
    action_url = reverse(action_url)
    return {
        'form': form,
        'action_url': action_url,
        'model_class': model_class
    }


@register.inclusion_tag('include/modal_update_form.html')
def model_form_update(action_url, instance, form):
    action_url = reverse(action_url, kwargs={'pk': instance.pk})
    return {
        'form': form,
        'action_url': action_url,
        'instance': instance,
    }


@register.inclusion_tag('include/modal_form_delete.html')
def model_form_delete(action_url, instance, redirect_url=None, redirect_pk=None):

    action_url = reverse(action_url, kwargs={'pk': instance.pk})
    if redirect_url:
        action_url += f"?redirect_url={redirect_url}"
    if redirect_pk:
        action_url += f"&redirect_pk={redirect_pk}"

    return {
        'instance': instance,
        'action_url': action_url,
        'instance_id': instance.pk,
        'instance_model_name': instance._meta.model_name,
    }


@register.filter
def get_field_value(obj, field_name):
    """
    Template filter to get a field's value from a model instance:
    - For DateTimeFields: returns date
    - For choice fields: returns get_FOO_display()
    - For ForeignKey/related fields: returns str(obj)
    - Else: returns raw value
    """
    try:
        field_value = getattr(obj, field_name)

        # Handle DateTimeField: return just the date
        if isinstance(field_value, datetime):
            return field_value.date()

        # Handle choice fields: call get_FOO_display() if available
        get_display_method = f"get_{field_name}_display"
        if hasattr(obj, get_display_method):
            return getattr(obj, get_display_method)()

        # Handle ForeignKeys or other related fields
        if field_value is not None and hasattr(field_value, '__str__'):
            return str(field_value)

        return field_value

    except AttributeError:
        return None



@register.filter
def format_field_name(value):
    """Format field names to be capitalized and space-separated."""
    # Convert snake_case to space-separated words and capitalize first letter
    value = re.sub(r'(_|\b)([a-zA-Z])', lambda m: ' ' + m.group(2).upper(), value).strip()
    return value


@register.filter
def action_urls_for(obj, user):
    return obj.get_action_urls(user)


@register.filter
def get_list_url(model_class, user):
    """
    Reversed: True
    Returns the list URL for the given model class based on its action URLs.
    """
    action_urls = model_class.get_action_urls(user)
    return reverse(action_urls.get("list")) if action_urls.get("list") else '#'


@register.filter
def get_create_url(model_class, user):
    """
    Reversed: False
    Returns the creation URL for the given model class based on its action URLs.
    """
    action_urls = model_class.get_action_urls(user)
    return action_urls.get("create", '/')


@register.filter
def get_detail_url(model_class, user):
    """
    Reversed: False
    Returns the detail URL for the given model class based on its action URLs.
    """
    action_urls = model_class.get_action_urls(user)
    return action_urls.get("detail", '/')


@register.filter
def create_action_url_for(model_class, user):
    return model_class.get_action_urls(user).get("create", None)


@register.filter
def get_verbose_name(model_class):
    return model_class._meta.verbose_name.title()


@register.filter
def get_model_name(model_class):
    return model_class._meta.model_name


@register.filter
def format_address(address):
    if not address:
        return ''
    # Replace ", " or "," with ",<br/>"
    return re.sub(r',\s*', ',<br/>', address)


@register.filter()
def badge_type(status):
    return {
        'draft': 'badge-light-warning',
        'sent': 'badge-info',
        'paid': 'badge-success',
        'overdue': 'badge-danger',
        'cancelled': 'badge-secondary',
        'refunded': 'badge-dark',
    }.get(status, 'badge-light')


@register.simple_tag
def detail_get_field_pairs(obj, field_names):
    result = []

    for field_name in field_names:
        try:
            field = obj._meta.get_field(field_name)
            label = field.verbose_name.capitalize()

            # Handle choices
            if hasattr(obj, f'get_{field_name}_display'):
                value = getattr(obj, f'get_{field_name}_display')()
            else:
                value = getattr(obj, field_name)

            # Handle FK or related objects
            if field.is_relation and value:
                value = str(value)

            result.append((label, value))
        except Exception:
            continue  # Skip invalid fields

    return result


@register.simple_tag(takes_context=True)
def pagination_update_query_param(context, key, value):
    """
    Update or add a query parameter while preserving the rest of the query string.
    """
    request = context['request']
    query = request.GET.copy()
    query[key] = value
    return '?' + urlencode(query)


def get_display_fields(user=None):
    """Return fields based on the user role."""
    fields = ['item_category', 'item', 'issue_by', 'issued_to']
    if user and user.is_staff:
        fields.append('is_active')  # Add is_active field for staff users
    return fields


@register.filter
def image_or_placeholder(image, placeholder=None):
    # https://api.dicebear.com/9.x/initials/svg
    # https://api.dicebear.com/9.x/initials/svg?size=32
    # https://api.dicebear.com/9.x/initials/svg?seed=Felix&size=100&radius=10
    if image:
        return image.url

    return "https://api.dicebear.com/9.x/glass/svg?seed=Felix"


@register.filter
def alert_type_class(value):
    if value in ['cod', 'delivery', 'in_transit', 'bank_account', "MANAGER", "trialing",'new']:
        return 'primary'
    if value in ['cod', 'delivery', 'in_transit', 'bank_account', "CASHIER", "incomplete", "incomplete_expired",'closed']:
        return 'info'
    elif value in ['completed', 'success', 'approved', 'paid', 'card', "OWNER", "active", "sent",'resolved']:
        return 'success'
    elif value in ['pending', "STAFF", "ADMIN", "past_due", "pause",'in_progress']:
        return 'warning'
    elif value in ['online', 'cancel', 'cancelled', 'unpaid', 'failed', "ROOT", "failed"]:
        return 'danger'
    else:
        return 'secondary'


@register.filter
def timeline_position(value):
    # if value % 2 == 0: return left else retrun right
    return 'left' if value % 2 == 0 else 'right'


@register.filter
def check_null(value):
    if value:
        return value
    return "-"


@register.filter
def check_null_2(value):
    if value:
        return value
    return ""


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price


@register.filter
def get_review_stars(value):
    html = ''
    active_stars = value
    inactive_stars = 5 - value

    for _ in range(active_stars):
        html += '<i class="active icofont-star"></i>'

    for _ in range(inactive_stars):
        html += '<i class="icofont-star"></i>'
    return html


@register.filter
def table_value_check_ui(value):
    if value:
        return '<i class="fa fa-check text-success"></i>'
    return '<i class="fa fa-times text-danger"></i>'


@register.filter(name='cool_num', is_safe=False)
def cool_number(value, num_decimals=2):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M, 1.2B, 5.7T...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """
    if value in (None, '', 'None'):
        return '0'

    try:
        int_value = float(value)
    except (ValueError, TypeError):
        return str(value)  # Fallback: return original string

    formatted_number = '{{:.{}f}}'.format(num_decimals)

    if int_value < 1000:
        return str(int(int_value))
    elif int_value < 1_000_000:
        return formatted_number.format(int_value / 1_000).rstrip('0').rstrip('.') + 'K'
    elif int_value < 1_000_000_000:
        return formatted_number.format(int_value / 1_000_000).rstrip('0').rstrip('.') + 'M'
    elif int_value < 1_000_000_000_000:
        return formatted_number.format(int_value / 1_000_000_000).rstrip('0').rstrip('.') + 'B'
    else:
        return formatted_number.format(int_value / 1_000_000_000_000).rstrip('0').rstrip('.') + 'T'


@register.filter
def check_permission(request, perms, permission_name):
    if request.user.is_superuser:
        return True
    return perms and perms.get(permission_name, False)


from django.utils.safestring import mark_safe


@register.filter
def bool_icon(value):
    if value in [True, 'True', 'true', 1, '1', 'Yes', 'yes', 'YES']:
        return mark_safe('<i class="mdi mdi-check text-success"></i>')

    return mark_safe('<i class="mdi mdi-close text-danger"></i>')


@register.filter
def pretty_json(value):
    try:
        return json.dumps(value, indent=2, ensure_ascii=False)
    except Exception as e:
        return value

@register.filter
def base_url(link):
    return BASE_URL + link


@register.filter(name='cool_num2', is_safe=False)
def cool_number2(value, num_decimals=2):
    """
    Formats a number with commas as thousands separator and specified decimal places.
    Input can be a number or string with commas.
    Output format: xxx,xxx,xxx.XX
    """
    try:
        # Remove commas if present and convert to float
        if isinstance(value, str):
            clean_value = float(value.replace(',', ''))
        else:
            clean_value = float(value)

        # Format the number
        formatted = f"{clean_value:,.{num_decimals}f}"

        # Ensure we don't have trailing .00 when num_decimals=0
        if num_decimals == 0:
            formatted = formatted.replace('.0', '')

        return formatted

    except (ValueError, TypeError, AttributeError):
        return str(value)

@register.simple_tag
def model_verbose_name(obj):
    model = obj if isinstance(obj, type) else obj.__class__
    return model._meta.verbose_name


@register.simple_tag
def model_verbose_name_plural(obj):
    model = obj if isinstance(obj, type) else obj.__class__
    return model._meta.verbose_name_plural


@register.simple_tag
def model_class_name(obj):
    model = obj if isinstance(obj, type) else obj.__class__
    return model._meta.model_name


@register.simple_tag
def model_app_name(obj):
    model = obj if isinstance(obj, type) else obj.__class__
    return model._meta.app_label.capitalize()
