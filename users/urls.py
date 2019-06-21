from .views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/logout/', LogoutView.as_view(), name="auth-logout")
]
