from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View

from src.apps.whisper.filters import EmailNotificationFilter
from src.apps.whisper.main import NotificationService
from src.apps.whisper.models import EmailNotification
from src.core.mixins import CustomPermissionMixin
from src.services.accounts.mixins import GenericListViewMixin


class EmailNotificationListView(GenericListViewMixin):
    model = EmailNotification
    filter_class = EmailNotificationFilter


class EmailNotificationRetryView(CustomPermissionMixin, View):
    permission_prefix = 'whisper'
    permission_action = 'change'

    def get_permission_name(self):
        return "whisper.change_emailnotification"

    def get(self, request, *args, **kwargs):
        email_notification_id = kwargs.get('pk')
        email_notification = get_object_or_404(EmailNotification, id=email_notification_id)

        notification_service = NotificationService(
            heading=email_notification.subject,
            description=email_notification.body,
            obj=email_notification.content_object,
            retry_id=email_notification.id,
            recipient_list=[email_notification.recipient]
        )

        context = {
            'body': email_notification.body
        }

        # Retry sending the email
        notification_service.send_email_notification_smtp(email_notification.template_name, context,
                                                     [email_notification.recipient])

        return redirect('whisper:emailnotification-list')
