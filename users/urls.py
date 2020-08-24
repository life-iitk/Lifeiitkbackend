from .views import *
from django.urls import path

urlpatterns = [
    path('', EditAPI),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/logout/', LogoutView.as_view(), name="auth-logout"),
    path('acads/', AcadsAPI),
    path('profile/', user_details),
    path('tags/',TagsAPI),
    path('owned/',OwnedTagAPI),
    path("course/delete/", DeleteAcadAPI),
    path("tags/delete/", UnsubscribeTagsAPI),
    path('verify/code=<str:token>/',SetPasswordAndActivate,name="email-activator"),
    path('register/',RegistrationView.as_view(),name="registration"),
    path('resetpassemail/',ResetPasswordEmail,name="resetpass-email"),
    path('resetpass/code=<str:token>/',ResetPassword,name="resetpass")
]
