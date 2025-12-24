import django_filters

from src.apps.whisper.models import EmailNotification


class EmailNotificationFilter(django_filters.FilterSet):

    recipient = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EmailNotification
        fields = ['recipient', 'status']