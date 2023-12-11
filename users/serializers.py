# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password1']

        # Создаем пользователя без сохранения
        user = User(username=username, email=email, is_active=0)
        user.set_password(password)
        user.save()
        return user
