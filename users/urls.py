from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from users.views import CustomRegisterAPIView

urlpatterns = [
    path('acc/', include('allauth.urls')),
    path('acc/register/', CustomRegisterAPIView.as_view(), name='custom_register'),
    # path('acc/verify-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
