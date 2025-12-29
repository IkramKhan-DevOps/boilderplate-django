from django.test import TestCase
from src.services.management.models import Country, State

class ManagementModelTest(TestCase):
    def test_country_creation(self):
        country = Country.objects.create(
            name='United States',
            short_name='US',
            language='en',
            currency='USD',
            phone_code='+1'
        )
        self.assertEqual(str(country), 'United States')
        self.assertTrue(country.is_active)

    def test_state_creation(self):
        country = Country.objects.create(name='United States', short_name='US')
        state = State.objects.create(name='California', country=country)
        self.assertEqual(str(state), 'California')
        self.assertEqual(state.country, country)
