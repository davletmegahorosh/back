from django.urls import path
from .views import Respone


urlpatterns = [
    path('', Respone.as_view()),


]
