from django.urls import path
from .views import GPTResponseApiView


urlpatterns = [
    path('', GPTResponseApiView.as_view()),


]
