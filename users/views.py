# users/views.py

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomRegisterSerializer
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from back import settings

User = get_user_model()


class CustomRegisterAPIView(CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']

        # Проверяем, существует ли пользователь с таким именем пользователя
        if User.objects.filter(username=username).exists():
            return Response({"detail": "This username is already taken. Please choose another one."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем пользователя и сохраняем
        user = serializer.save()
        user.set_password(serializer.validated_data['password1'])
        user.save()

        # Генерация кода и сохранение его в модели пользователя
        code = get_random_string(length=6)
        user.verification_code = code
        user.save()

        # Отправка кода на почту
        subject = 'Verification Code'
        message = f'Your verification code is: {code}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        return Response({"detail": "Verification code has been sent to your email."}, status=status.HTTP_201_CREATED)
