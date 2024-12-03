from rest_framework import serializers

from src.services.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'email', 'username', 'first_name', 'last_name'
        ]
        read_only_fields = ['pk', 'email']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)

