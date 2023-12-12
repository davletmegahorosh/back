from rest_framework import serializers
from .models import CustomUsers
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    username = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.'),
                    UniqueValidator(queryset=CustomUsers.objects.all(), message='This username is already in use.')]
    )

    class Meta:
        model = CustomUsers
        fields = ['username', 'email', 'password']

    def validate(self, data):
        return data

    def create(self, validated_data):
        # Generate a 4-digit numeric confirmation code
        confirmation_code = get_random_string(length=4, allowed_chars='0123456789')

        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_active=False,  # Устанавливаем активность пользователя в False до подтверждения
            confirmation_code=confirmation_code,
        )

        # Отправка электронной почты с кодом подтверждения
        subject = 'Confirmation code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = 'bapaevmyrza038@gmail.com'  # Укажите ваш отправительский email
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return user



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    new_password = serializers.CharField(write_only=True, required=True)