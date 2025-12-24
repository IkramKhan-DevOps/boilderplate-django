from django.urls import path, include
from .views import (
    UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserCreateView, UserPasswordResetView,
    LogoutView, CrossAuthView, UserUpdateFullView, UserPasswordChangeView, UserGroupPermissionCreateView,
    UserGroupPermissionUpdateView, UserGroupPermissionDeleteView, UserPermissionUpdate,
)

app_name = 'accounts'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),
    # path('signup/', SignUpView.as_view(), name='account-signup'),
]

urlpatterns += [
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>/update/', UserUpdateFullView.as_view(), name='user_update_full'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),
    path('user/password/change/', UserPasswordChangeView.as_view(), name='user-password-change-view'),
]

urlpatterns += [
    path('permission/add/', UserGroupPermissionCreateView.as_view(), name='permission_add'),
    path('permission/<int:pk>/update/', UserGroupPermissionUpdateView.as_view(), name='permission_update'),
    path('permission/<int:pk>/delete/<int:user_id>/', UserGroupPermissionDeleteView.as_view(),
         name='permission_delete'),
    path('user/<int:pk>/permission/update/', UserPermissionUpdate.as_view(), name='user_permission_update'),
]

