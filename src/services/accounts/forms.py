from django.contrib.auth import get_user_model
from django.forms import ModelForm


class UserProfileForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'profile_image', 'first_name', 'last_name',
            'phone_number'
        ]

