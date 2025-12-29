from django.test import TestCase
from src.services.accounts.models import User, UserType

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, UserType.client)
        self.assertTrue(user.is_active)

    def test_user_str(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(user), 'John Doe')

        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com'
        )
        self.assertEqual(str(user2), 'testuser2')

    def test_staff_user_type(self):
        user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            is_staff=True
        )
        # Note: save() logic sets it to administration if staff/superuser
        self.assertEqual(user.user_type, UserType.administration)
