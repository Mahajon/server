# example/views.py
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets
#import authenticate
from django.contrib.auth import authenticate
from .serializers import UserSerializer
import json

def LoginView(request):
    # get the username and password from the request
    # authenticate the user
    try:
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            return HttpResponse(f"Hello, {user.email}!", status=status.HTTP_200_OK)
        else:
            raise Exception("Unauthorized")
    except Exception as e:
        return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
    

class UserViewSet(viewsets.ViewSet):
    def get(self, request):
        try:
            user = request.user
            print(user)
            if user is not None:
                serializer = UserSerializer(user)
                print(serializer.data)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            else:
                raise Exception("Unauthorized")
        except Exception as e:
            print(e)
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self, request):
        # get the bearer token from request Authorization header
        # authenticate the user
        user = authenticate(request)
        if user is not None:
            #update the user's last login time
            user.last_login = datetime.now()
            user.save()
            return HttpResponse(f"Last login time updated for {user.username}", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)