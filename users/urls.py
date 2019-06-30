from .views import LoginView, LogoutView, EditAPI, AcadsAPI, user_details, TagsAPI ,OwnedTagAPI
from django.urls import path

urlpatterns = [
    path('', EditAPI),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/logout/', LogoutView.as_view(), name="auth-logout"),
    path('acads/', AcadsAPI),
    path('profile/', user_details),
    path('tags/',TagsAPI),
    path('owned/',OwnedTagAPI)
]
