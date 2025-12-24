from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
import re
from django.core.exceptions import ValidationError

def phone_number_validator(value):
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError('Phone number must be in the format (xxx) xxx-xxxx')

def phone_number_null_or_validator(value):
    if value is None or value == '':
        return
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError('Phone number must be in the format (xxx) xxx-xxxx')

def validate_us_zip_code(value):
    """
    Validates that the value is a valid US ZIP code:
    - 5 digits (e.g., 12345)
    - or ZIP+4 format (e.g., 12345-6789)
    """
    if value is None or value == '':
        return
    zip_regex = re.compile(r'^\d{5}(-\d{4})?$')
    if not zip_regex.match(value):
        raise ValidationError("Enter a valid US ZIP code (e.g., 12345 or 12345-6789).")

def phone_extension_validator(value):
    """
    Validates that a phone extension is 2-6 digits (optional field).
    """
    if value in [None, '']:
        return
    if not re.match(r'^\d{2,6}$', value):
        raise ValidationError("Enter a valid phone extension (2-6 digits).")


""" PLATFORMS """


def domain_validator(value):

    if value in ['127.0.0.1:8000', '127.0.0.1:8080']:
        return

    if not isinstance(value, str):
        raise ValidationError('Domain must be a string.')
    value = value.strip()
    if value.startswith('http://') or value.startswith('https://'):
        raise ValidationError('Domain should not include protocol (http:// or https://).')
    if '/' in value:
        raise ValidationError('Domain should not contain any path or trailing slash.')
    if ':' in value:
        raise ValidationError('Domain should not include port numbers.')

    # Basic domain regex (does not cover all cases, but blocks obvious mistakes)
    if not re.match(r'^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$', value):
        raise ValidationError('Enter a valid domain name.')


def protocol_validator(value):
    if not isinstance(value, str):
        raise ValidationError('Protocol must be a string.')
    value = value.lower()
    if value not in ['http', 'https']:
        raise ValidationError('Protocol must be either "http" or "https".')




class Application(models.Model):
    name = models.CharField(max_length=100, help_text='Application name', default='Exarth')
    short_name = models.CharField(max_length=10, help_text='Your application short name', default='EX')
    tagline = models.CharField(
        max_length=100, help_text='Your application business line', default='Your digital partner'
    )
    description = models.TextField(
        default="Your technology partner in innovations, automation and business intelligence.",
        help_text='Application description'
    )

    favicon = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='Application favicon'
    )
    logo = models.ImageField(
        upload_to='core/application/images', null=True, blank=True,
        help_text='Application real colors logo'
    )
    logo_dark = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='For dark theme only'
    )
    logo_light = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='For light theme only'
    )

    contact_email1 = models.EmailField(
        max_length=100, default='support@exarth.com', help_text='Application contact email 1'
    )
    contact_email2 = models.EmailField(
        max_length=100, default='support@exarth.com', help_text='Application contact email 2'
    )
    contact_phone1 = PhoneNumberField(
        help_text='Application contact phone 1', default='+923419387283'
    )
    contact_phone2 = PhoneNumberField(
        help_text='Application contact phone 2', default='+923259575875'
    )

    address = models.CharField(
        max_length=255, help_text='office address', default='123 Main St, Abbotabad, KPK Pakistan'
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=6, help_text='latitude', default=23.7)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, help_text='longitude', default=90.3)

    terms_url = models.URLField(
        max_length=255, default='https://exarth.com/terms-of-use/', help_text='Terms and Conditions page link'
    )

    version = models.CharField(max_length=10, help_text='Current version', default='1.0.0')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Application"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if Application.objects.exists() and not self.pk:
            raise ValidationError("Only one record allowed.")
        super(Application, self).save(*args, **kwargs)



