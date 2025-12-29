from django.core.mail import send_mail
from django.db.models import F
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

from root.settings import EMAIL_HOST_USER, MAILCHIMP_FROM_EMAIL, MAILCHIMP_API_KEY
from src.apps.whisper.models import EmailNotification


class NotificationService:

    def __init__(self, heading, description, obj=None, recipient_list=None, retry_id=None):
        self.recipient_list = recipient_list or []
        self.heading = heading
        self.obj = obj
        self.description = description
        self.retry_id = retry_id
        self.email_id = []

    def create_notification_record(self, emails, status='pending', template_name=None, error_message=None):
        notifications = [
            EmailNotification(
                subject=self.heading,
                body=self.description,
                recipient=recipient,
                status=status,
                template_name=template_name,
                error_message=error_message,
                content_object=self.obj
            ) for recipient in emails
        ]
        created_notifications = EmailNotification.objects.bulk_create(notifications)
        self.email_id.extend([obj.id for obj in created_notifications])

    def update_notification_record(self, ids, status, error_message=None):
        queryset = EmailNotification.objects.filter(id__in=ids)
        if status == 'failed':
            queryset.update(
                status=status,
                error_message=error_message,
                failed_attempts=F('failed_attempts') + 1
            )
        else:
            queryset.update(
                status=status,
                error_message=error_message
            )

    def send_email_notification_smtp(self, template, context, email=None):
        email_list = [email] if email else [user.email for user in self.recipient_list]
        if email_list:
            if not self.retry_id:
                self.create_notification_record(email_list, template_name=template)
            else:
                self.email_id.append(self.retry_id)

            try:
                html_message = render_to_string(template, context)
                plain_message = strip_tags(html_message)
                from_email = EMAIL_HOST_USER
                send_mail(
                    self.heading,
                    plain_message,
                    from_email,
                    email_list,
                    html_message=html_message
                )
                self.update_notification_record(self.email_id, 'sent')
            except Exception as e:
                self.update_notification_record(self.email_id, 'failed', error_message=str(e))

    def send_email_notification(self, template, context, email=None):
        mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
        email_list = [{"email": recipient} for recipient in email] if email else [{"email": user.email} for user in self.recipient_list]

        if email_list:
            if not self.retry_id:
                self.create_notification_record([recipient['email'] for recipient in email_list], template_name=template)
            else:
                self.email_id.append(self.retry_id)

            try:
                message = {
                    "from_email": MAILCHIMP_FROM_EMAIL,
                    "subject": self.heading,
                    "to": email_list,
                    "global_merge_vars": [{"name": "description", "content": self.description}],
                    "template_name": template,
                    "html": render_to_string(template, context)
                }
                mailchimp.messages.send({"message": message})
                self.update_notification_record(self.email_id, 'sent')
            except ApiClientError as error:

                self.update_notification_record(self.email_id, 'failed', error_message=error.text)

    def send_app_notification(self):
        pass

    def send_sms_notification(self):
        pass

    def send_push_notification(self):
        pass
