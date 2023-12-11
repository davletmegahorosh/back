# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from .serializers import *
# from . models import ConfirmationCode
# from djoser.views import UserViewSet as DjoserUserViewSet

# class RegistrationAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegistrationSerializer
#     # permission_classes = (AllowAny)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_201_CREATED)
#
#     def perform_create(self, serializer):
#         return serializer.save()



# def save_confirmation_code_in_database(email, confirmation_code):
#     user = User.objects.get(email=email)
#
#     confirmation_obj, created = ConfirmationCode.objects.get_or_create(user=user, defaults={'code': confirmation_code})
#
#     if not created:
#         confirmation_obj.code = confirmation_code
#         confirmation_obj.save()
# class CustomRegistrationView(DjoserUserViewSet):
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         confirmation_code = generate_confirmation_code()
#
#         send_confirmation_email(request.data['email'], confirmation_code)
#
#         save_confirmation_code_in_database(request.data['email'], confirmation_code)
#
#         return Response({'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)
#
# def generate_confirmation_code():
#     return '123456'
#
# def send_confirmation_email(email, confirmation_code):
#     subject = 'Код подтверждения регистрации'
#     message = f'Ваш код подтверждения: {confirmation_code}'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)
