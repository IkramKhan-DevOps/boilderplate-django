from django.contrib import messages
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, UpdateView, CreateView, DeleteView, ListView, TemplateView
from django.contrib.auth import logout, get_user_model

from .filters import UserFilter
from .forms import UserCreateForm, UserUpdateForm, UserUpdateLimitedForm, GroupForm
from .mixins import StaffMixin, SuperUserMixin
from .models import User
from ...core.mixins import CustomPermissionMixin


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


class CrossAuthView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('dashboard:dashboard')


class UserListView(StaffMixin, CustomPermissionMixin, ListView):
    model = User
    paginate_by = 50
    filter_class = UserFilter
    permission_prefix = 'accounts'
    permission_action = 'view'
    queryset = User.objects.all().order_by('-date_joined')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filter_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        return context


class UserDetailView(StaffMixin, CustomPermissionMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    permission_prefix = 'accounts'
    permission_action = 'view'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        if self.request.user.is_superuser:
            user_permissions = user.user_permissions.all()
            all_permissions = Permission.objects.select_related('content_type').all()
            
            for permission in all_permissions:
                permission.checked = permission in user_permissions

            user_groups = user.groups.all()
            all_groups = Group.objects.all()

            for group in all_groups:
                group.checked = group in user_groups

            context['permission_list'] = all_permissions
            context['group_permission_list'] = all_groups

        return context


class UserCreateView(StaffMixin, CustomPermissionMixin, CreateView):
    model = User
    form_class = UserCreateForm
    permission_prefix = 'accounts'
    permission_action = 'add'

    def get_success_url(self):
        messages.success(self.request, "User created successfully.")
        return reverse_lazy('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserUpdateView(StaffMixin, CustomPermissionMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    permission_prefix = 'accounts'
    permission_action = 'change'

    def get_success_url(self):
        messages.success(self.request, "User updated successfully.")
        return self.request.META.get('HTTP_REFERER', '/')


class UserUpdateFullView(LoginRequiredMixin, CustomPermissionMixin, UpdateView):
    model = User
    permission_prefix = 'accounts'
    permission_action = 'change'

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        if request.user.is_staff or request.user == user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("You are not allowed to perform this action")

    def get_form_class(self):
        if self.request.user.is_staff:
            return UserUpdateForm
        return UserUpdateLimitedForm

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully.")
        return self.request.META.get('HTTP_REFERER', '/')


class UserDeleteView(StaffMixin, CustomPermissionMixin, DeleteView):
    model = User
    permission_prefix = 'accounts'
    permission_action = 'delete'
    success_url = reverse_lazy('accounts:user_list')


class UserPasswordResetView(StaffMixin, CustomPermissionMixin, View):
    model = User
    permission_prefix = 'accounts'
    permission_action = 'change'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'accounts/admin_password_reset.html', {'form': form, 'object': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()} password changed successfully.")
        return render(request, 'accounts/admin_password_reset.html', {'form': form, 'object': user})


class UserPasswordChangeView(LoginRequiredMixin, CustomPermissionMixin, View):
    model = User
    permission_prefix = 'accounts'
    permission_action = 'change'

    def get(self, request):
        user = request.user
        form = PasswordChangeForm(user=user)
        return render(request, 'accounts/user_password_change.html', {'form': form, 'object': user})

    def post(self, request):
        user = request.user
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Your password changed successfully.")
        return render(request, 'accounts/user_password_change.html', {'form': form, 'object': user})


class UserPermissionUpdate(SuperUserMixin, View):
    def post(self, request, *args, **kwargs):
        user_permission_ids = request.POST.getlist('permissions')
        group_permission_ids = request.POST.getlist('group_permissions')
        user = get_object_or_404(get_user_model(), id=self.kwargs.get('pk'))
        user.user_permissions.set(user_permission_ids)
        user.groups.clear()
        for group in group_permission_ids:
            user.groups.add(group)
        messages.success(request, f"Permission Successfully Updated for {user}")
        return redirect('accounts:user_detail', pk=self.kwargs.get('pk'))


class UserGroupPermissionCreateView(SuperUserMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_form.html'
    success_url = reverse_lazy('accounts:permission_add')

    def form_valid(self, form):
        messages.success(self.request, "Group Successfully Added ")
        return super().form_valid(form)


class UserGroupPermissionUpdateView(SuperUserMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group_form.html'
    success_url = reverse_lazy('accounts:permission_add')

    def form_valid(self, form):
        messages.success(self.request, "Group Successfully Updated ")
        return super().form_valid(form)


class UserGroupPermissionDeleteView(SuperUserMixin, DeleteView):
    model = Group
    template_name = 'accounts/group_delete.html'

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Group Successfully Deleted")
        user_id = self.kwargs.get('user_id')
        return reverse_lazy('accounts:user_detail', kwargs={'pk': user_id})
