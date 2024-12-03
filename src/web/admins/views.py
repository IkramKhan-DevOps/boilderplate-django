from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView
)

# from faker_data import initialization
from src.services.users.models import User
from src.web.accounts.decorators import staff_required_decorator
from src.web.admins.filters import UserFilter


@method_decorator(staff_required_decorator, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context = calculate_statistics(context)
        # initialization(init=False, mid=False, end=False)
        return context


""" USERS """


@method_decorator(staff_required_decorator, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


def post(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = AdminPasswordChangeForm(data=request.POST, user=user)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
    return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})


@method_decorator(staff_required_decorator, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})


""" SOCIALS """

from allauth.socialaccount.models import SocialAccount
from django.views.generic import TemplateView


class SocialsView(TemplateView):
    template_name = 'admins/social-accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['social_accounts'] = SocialAccount.objects.filter(user=self.request.user)
        return context


@login_required
def remove_social_account(request, account_id):
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
    account.delete()
    return redirect('admins:social-accounts')  # Update with your actual view name or URL name
