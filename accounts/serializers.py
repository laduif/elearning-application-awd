from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
            'profile_picture',
        )

        read_only_fields = (
            'id',
            'username',
            'role',
        )