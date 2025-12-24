from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML


class UserCreateForm(UserCreationForm):

    class Meta:
        model = get_user_model()  # Replace with your custom User model if needed
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "user_type",
            "is_staff",
            "is_superuser",
            "is_active",
            "password1",
            "password2",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Marcus"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Merlin"}),
            "email": forms.EmailInput(attrs={"placeholder": "admin@exarth.com"}),
            "username": forms.TextInput(attrs={"placeholder": "admin"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('user_type', css_class='form-group col-md-3 mb-0'),
                Column('is_staff', css_class='form-group col-md-3 mb-0'),
                Column('is_superuser', css_class='form-group col-md-3 mb-0'),
                Column('is_active', css_class='form-group col-md-3 mb-0'),
            ),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.user_type = self.cleaned_data["user_type"]
        user.platform = self.cleaned_data["platform"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.is_active = self.cleaned_data["is_active"]
        if commit:
            user.save()
        return user


class UserUpdateForm(ModelForm):

    class Meta:
        model = get_user_model()  # Replace with your custom User model if needed
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "user_type",
            "is_staff",
            "is_superuser",
            "is_active",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Marcus"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Merlin"}),
            "email": forms.EmailInput(attrs={"placeholder": "admin@exarth.com"}),
            "username": forms.TextInput(attrs={"placeholder": "admin"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('user_type', css_class='form-group col-md-4 mb-0'),
                Column('is_staff', css_class='form-group col-md-4 mb-0'),
                Column('is_superuser', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),
            ),
        )


""" OTHER """


class UserProfileForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'profile_image', 'first_name', 'last_name',
            'phone_number'
        ]


class UserUpdateLimitedForm(ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = get_user_model()
        fields = ['profile_image', 'first_name', 'last_name', 'phone_number']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


