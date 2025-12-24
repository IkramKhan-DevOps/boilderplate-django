from django.urls import path
from .views import LogoutView, CrossAuthView, UserUpdateView, UserListView, UserDetailView, UserPasswordResetView

app_name = 'accounts'
urlpatterns = [

    path('logout/', LogoutView.as_view(), name='logout'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

]
