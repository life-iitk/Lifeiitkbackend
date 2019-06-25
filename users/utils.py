from .models import User


def IsLoggedIn(request):
    if request.session.has_key("username"):
        try:
            user = User.objects.get(username=request.session["username"])
            return user

        except:
            return None
    else:
        return None
