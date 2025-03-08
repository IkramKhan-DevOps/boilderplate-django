
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from django.urls import reverse
from django.http import HttpResponseRedirect


class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        return resolve_url('account_set_password')

    def get_login_redirect_url(self, request):
        # Check if the user has a usable password
        user = request.user
        if user.is_authenticated and user.has_usable_password():
            return resolve_url('/')

        else:
            return resolve_url('account_set_password')


    def respond_user_authenticated(self, request, user):
        """
        Called when a user is authenticated successfully.
        """
        # Redirect based on whether the user has a usable password
        if user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        else:
            return HttpResponseRedirect(reverse('/'))
