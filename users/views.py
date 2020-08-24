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
from .utils import *
import json
from django.views.decorators.csrf import csrf_exempt
from tokens.models import Token
from lifeiitkbackend.settings_email import *
import bcrypt
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
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
            user = User.objects.get(username = username, activated = True)
            if user is not None:
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    request.session["username"] = username 
                    request.session.modified = True
                    t = Token.objects.filter(token = token)
                    if len(t) == 0 and token != "undefined":
                        newtoken = Token(token = token)
                        newtoken.save()
                        newtoken.user.add(user)
                        newtoken.save()
                    return Response(status = status.HTTP_200_OK)
                else:
                    return Response(status = status.HTTP_401_UNAUTHORIZED)
            
        except :
            return Response(status = status.HTTP_401_UNAUTHORIZED)

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

class RegistrationView(APIView):
    
    def post(self, request):
        if IsRegistered(request) is False:
            ActivationMailer(request)
            return Response(status = status.HTTP_202_ACCEPTED)
        if IsRegistered(request) is True:
            return Response(status = status.HTTP_403_FORBIDDEN)
        if IsRegistered(request) is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(status = status.HTTP_400_BAD_REQUEST)
def ActivationMailer(request): 
    if request.method == "POST":
        try:
            roll_no = request.data['roll']
            user_data = User.objects.get(roll = roll_no)
            sender = EMAIL_HOST_USER
            name = user_data.username
            recipient = name + "@iitk.ac.in"
            user_code = user_data.generate_verification_code()
            user_link = EMAIL_LINK["Activation"].format(code = user_code)
            subject = EMAIL_SUBJECT["Activation"]
            body = EMAIL_BODY["Activation"].format(name=name, link=user_link)
            send_mail(subject, body, sender, [recipient], fail_silently=False)
            return redirect(REDIRECT_LINK["Activation"])
        except:
            return HttpResponse("Please set up email host details!", status=206)
    else :
        return HttpResponse("Invalid request!", status=400)

def HashPass(password):
    password=password.encode()
    return bcrypt.hashpw(password,bcrypt.gensalt())

@api_view(['POST'])
def SetPasswordAndActivate(request,token):
    if request.method == "POST":
        try:
            pw=request.data['password']
            user_data=User.objects.get(verification_code=token)
            if user_data.activated==False:
                user_data.activated=True
                user_data.password=HashPass(pw).decode()
                user_data.save()
                response={
                    'status':'success',
                    'code':status.HTTP_200_OK,
                    'message':'Password set succesfully and now you are registered',
                }
                return Response(response)
            else:
                response={
                'code':'status.HTTP_401_UNAUTHORIZED',
                'message':'Token already used'}
                return Response(response,status=401)  
        except:
            response={
                    'code':'status.HTTP_401_UNAUTHORIZED',
                    'message':'Invalid token or invalid request'
                }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse("Invalid Request",status=400)

@api_view(['POST'])
def ResetPasswordEmail(request):
    if request.method == "POST":
        try:
            roll_no = request.data['roll']
            user_data = User.objects.get(roll = roll_no)
            sender = EMAIL_HOST_USER
            name = user_data.username
            recipient = name + "@iitk.ac.in"
            user_code = user_data.generate_verification_code()
            user_link = EMAIL_LINK["PasswordReset"].format(code = user_code)
            subject = EMAIL_SUBJECT["PasswordReset"]
            body = EMAIL_BODY["PasswordReset"].format(name=name, link=user_link)
            send_mail(subject, body, sender, [recipient], fail_silently=False)
            return redirect(REDIRECT_LINK["PasswordReset"])
        except:
            return HttpResponse("Please set up email host details!", status=206)
    else :
        return HttpResponse("Invalid request!", status=400)

def pass_checker(old,password):
    return bcrypt.checkpw(old.encode(),password)

@api_view(['POST'])
def ResetPassword(request,token):
    if request.method == "POST":
        try:
            new1=request.data['new_password1']
            new2=request.data['new_password2']
            old=request.data['old_password']
            user_data=User.objects.get(verification_code=token)
            password=(user_data.password)
            password=password.encode()
            if user_data.activated==True:
                if(new1==new2):
                    if(pass_checker(old,password)==True):
                        user_data.password=HashPass(new1).decode()
                        user_data.save()
                        response={
                            'status':'success',
                            'code':status.HTTP_200_OK,
                            'message':'Password reset succesfull and now you can login',
                        }
                        return Response(response)
                    else:
                        response={
                            'status':'failure',
                            'code':status.HTTP_401_UNAUTHORIZED,
                            'message':'wrong old password',
                        }
                        return Response(response)
                else:
                    response={
                        'status':'failure',
                        'code':401,
                        'message':"the retyped password doesn't match",
                    }
                    return Response(response)

            else:
                response={
                'code':'status.HTTP_401_UNAUTHORIZED',
                'message':'Unauthorised user or Account not activated'}
                return Response(response,status=401)  
        except:
            response={
                    'code':'status.HTTP_401_UNAUTHORIZED',
                    'message':'Invalid token or invalid request'
                }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse("Invalid Request",status=400) 
