from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from utils import tokenOps
# Create your views here.
# success: {code:0,message:""}


@require_POST
def Login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    if username is not None and password is not None:
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token= tokenOps.create_token(username)
            response = JsonResponse({"code":0, "message":"","data":{"token": token}})
            return response
        else:
            return JsonResponse({"code":1, "message":"密码或用户名错误"})


def getUser(request):
    token = request.GET.get("token")
    username = tokenOps.get_username(token)
    users = {
        'admin-token': {
            "roles": ['admin'],
            "introduction": 'I am a super administrator',
            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            "name": username
        }
    }
    return JsonResponse({"code":0,"data":users['admin-token']})


def Logout(request):
    logout(request)
    return JsonResponse({"code":0,"message":"success"})
