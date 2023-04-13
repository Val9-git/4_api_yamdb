from django.urls import path

from .views import RegistrationAPIView

app_name = 'users'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
]