from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from imaplib import IMAP4
from .models.users import User


class LoginView(APIView):
    """
    POST auth/login/
    """
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        try:
            c = IMAP4('newmailhost.cc.iitk.ac.in')
            c.login(username, password)     #If user can authenticate then he is in our database
        except:
            return Response(status = status.HTTP_401_UNAUTHORIZED)              #Login fails

        user = User.objects.get(username=username)
        
        if user is not None:
            request.session["username"] = username                      #Starting session manually
            return Response(status = status.HTTP_200_OK)
        
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        if request.session.has_key("username"):
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_200_OK)


class LogoutView(APIView):
    
    def get(self, request):
        if request.session.has_key("username"):
            del request.session["username"]
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)              #Trying to logout without logging in
        