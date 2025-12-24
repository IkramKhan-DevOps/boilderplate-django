from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView, ListView, UpdateView, CreateView
from django.contrib.auth import logout

from .decorators import staff_required_decorator
from .filters import UserFilter
from .models import User


""" AUTH VIEWS """


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('account_login')

        if request.user.is_staff:
            return redirect('admins:dashboard')

        if request.user.is_superuser:
            return redirect('/admin/')

        return redirect('/')


""" USER VIEWS """


@method_decorator(login_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]


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

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(staff_required_decorator, name='dispatch')
class UserPasswordResetView(UpdateView):
    model = User
    form_class = AdminPasswordChangeForm
    template_name = 'accounts/password_reset.html'

    def get_success_url(self):
        messages.success(self.request, 'Password has been reset successfully.')
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})