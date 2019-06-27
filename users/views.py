from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from imaplib import IMAP4
from .models.users import User
from rest_framework.decorators import api_view
from acads.models import AcadsModel
from .Serializer import UserSerializer
from django.http import JsonResponse
from tags.models import TagModel
from .utils import IsLoggedIn

class LoginView(APIView):
    """
    POST auth/login/
    """
    
    def post(self, request, *args, **kwargs):
        user = IsLoggedIn(request)
        if user is not None :
            return Response(status = status.HTTP_400_BAD_REQUEST)
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        try:
            c = IMAP4('newmailhost.cc.iitk.ac.in')
            c.login(username, password)     #If user can authenticate then he is in our database
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)              #Login fails

        user = User.objects.get(username=username)
        
        if user is not None:
            request.session["username"] = username                      #Starting session manually
            return Response(status = status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        if IsLoggedIn(request) is not None:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_200_OK)


class LogoutView(APIView):
    
    def get(self, request):
        if IsLoggedIn(request) is not None:
            del request.session["username"]
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)              #Trying to logout without logging in


@api_view(['PUT', ])
def EditAPI(request):
    if request.method == 'PUT':
        user = IsLoggedIn(request)
        if user is not None:
            if len(request.data["fblink"]) != 0:
                user.fblink = request.data.get("fblink", "")
                fb = request.data.get("fblink","")
                user.fblink = fb
                user.save()
                return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(status = status.HTTP_401_UNAUTHORIZED)


def AcadsAPI(request):
    if request.method=='PUT':
        user = IsLoggedIn(request)
        if user is not None:
            request.session["username"] = user.username                      #Starting session manually
            a = AcadsModel.objects.get(course_id = request.data.get("course_id"))
            if a is not None:
                user.acads.add(a)
                user.save()
                return Response(status= status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_401_UNAUTHORIZED)

            
@api_view(['PUT', ])
def TagsAPI(request):
    if request.method=='PUT':
        user = IsLoggedIn(request)
        if user is not None:
            request.session["username"] = user.username                      #Starting session manually
            t = TagModel.objects.get(tag_id = request.data.get("tag_id"))
            if t is not None:
                user.tags.add(t)
                user.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(status= status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_401_UNAUTHORIZED)

@api_view(('GET',))
def user_details(request):
    user = IsLoggedIn(request)
    if user is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)
