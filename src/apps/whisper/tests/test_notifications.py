from django.test import TestCase
from django.core import mail
from src.apps.whisper.models import EmailNotification
from src.apps.whisper.main import NotificationService
from django.contrib.auth import get_user_model

User = get_user_model()

class WhisperTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_notification_service_bulk_create(self):
        service = NotificationService(
            heading="Test Heading",
            description="Test Description",
            recipient_list=[self.user]
        )
        
        # Test smtp sending (will create record)
        service.send_email_notification_smtp("whisper/email/email.html", {"body": "test"}, email="test1@example.com")
        
        self.assertEqual(EmailNotification.objects.count(), 1)
        notification = EmailNotification.objects.first()
        self.assertEqual(notification.recipient, "test1@example.com")
        self.assertEqual(notification.status, "sent")
        self.assertEqual(len(mail.outbox), 1)

    def test_notification_service_multiple_recipients(self):
        service = NotificationService(
            heading="Bulk Test",
            description="Bulk Description"
        )
        emails = ["one@example.com", "two@example.com"]
        service.create_notification_record(emails)
        
        self.assertEqual(EmailNotification.objects.count(), 2)
        self.assertEqual(len(service.email_id), 2)
        
    def test_update_notification_record(self):
        n = EmailNotification.objects.create(
            subject="Sub", body="Body", recipient="test@example.com", status="pending"
        )
        service = NotificationService("Sub", "Body")
        service.update_notification_record([n.id], "failed", error_message="Error")
        
        n.refresh_from_db()
        self.assertEqual(n.status, "failed")
        self.assertEqual(n.failed_attempts, 1)
        self.assertEqual(n.error_message, "Error")
