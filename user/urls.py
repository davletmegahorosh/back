from django.urls import path, include
# from .views import CustomRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    # path('custom-register/', CustomRegistrationView.as_view()),
    # path('register/', RegistrationAPIView.as_view()),
    # path('djoser/', include('djoser.urls')),
    # path('djoser/', include('djoser.urls.jwt')),
    # path(r'^auth/', include('djoser.urls.authtoken'))
]
