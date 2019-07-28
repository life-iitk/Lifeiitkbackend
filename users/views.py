from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from imaplib import IMAP4
from .models.users import User
from rest_framework.decorators import api_view
from acads.models import AcadsModel
from .Serializer import UserSerializer , UserOwnedSerializer, UserAcadsSerializer
from django.http import JsonResponse
from tags.models import TagModel
from .utils import IsLoggedIn
import json
from django.views.decorators.csrf import csrf_exempt
from tokens.models import Token

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
        token = request.data.get("token","")
        try:
            c = IMAP4('newmailhost.cc.iitk.ac.in')
            c.login(username, password)     #If user can authenticate then he is in our database
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)              #Login fails

        user = User.objects.get(username=username)
        
        if user is not None:
            request.session["username"] = username 
            request.session.modified = True                     #Starting session manually
            t = Token.objects.filter(token = token)
            if len(t) == 0 and token != "undefined":
                newtoken = Token(token = token)
                newtoken.save()
                newtoken.user.add(user)
                newtoken.save()
            return Response(status = status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if IsLoggedIn(request) is not None:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_200_OK)


class LogoutView(APIView):
    
    def post(self, request):
        if IsLoggedIn(request) is not None:
            token = request.data.get("token")
            dtoken = Token.objects.filter(token = token)
            if len(dtoken) !=0 :
                dtoken[0].delete()
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

@csrf_exempt
def AcadsAPI(request):
    if request.method=='PUT':
        user = IsLoggedIn(request)
        if user is not None:
            request.session["username"] = user.username
            data = json.loads(request.body)
            code = data["code"]
            a = AcadsModel.objects.get(code = code)
            if a is not None:
                user.acads.add(a)
                user.save()
                return JsonResponse({'status': 'ok'}, status=200)
            else:
                return JsonResponse({'Error': 'Bad Request'}, status=400)
        return JsonResponse({'Error': 'Unauthorized'}, status=401)
    elif request.method=='GET':
        user = IsLoggedIn(request)
        if user is None:
            HttpResponse(status=204)
        serializer = UserAcadsSerializer(user)

        return JsonResponse(serializer.data)
@csrf_exempt
def TagsAPI(request):
    if request.method=='PUT':
        user = IsLoggedIn(request)
        if user is not None:
            request.session["username"] = user.username
            data = json.loads(request.body)
            name = data["name"]
            t = TagModel.objects.filter(name = name)
            if t.exists():
                user.tags.add(t[0])
                user.save()
                return JsonResponse({'status': 'ok'}, status=200)
            else:
                return JsonResponse({'Error': 'Bad Request'}, status=400)
        return JsonResponse({'Error': 'Unauthorized'}, status=401)

@api_view(['GET',])
def user_details(request):
    if request.method=='GET':
        user = IsLoggedIn(request)
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
@api_view(['GET'])
def OwnedTagAPI(request):
    if request.method=='GET':
        user = IsLoggedIn(request)
        if user is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserOwnedSerializer(user)

        return JsonResponse(serializer.data)

@api_view(["DELETE"])
def DeleteAcadAPI(request):
    if request.method == "DELETE":
        user = IsLoggedIn(request)
        if user is not None:
            course_code = request.data.get("code")
            course = user.acads.filter(code=course_code)
            print(course)
            if course.exists():
                user.acads.remove(course[0])
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(["DELETE"])
def UnsubscribeTagsAPI(request):
    if request.method == "DELETE":
        user = IsLoggedIn(request)
        if user is not None:
            tag_id = request.data.get("tag_id")
            tag = user.tags.filter(tag_id=tag_id)
            if tag.exists():
                user.tags.remove(tag[0])
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
