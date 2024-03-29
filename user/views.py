# example/views.py
from datetime import datetime
from django.http import HttpResponse
from rest_framework import status, viewsets
#import authenticate
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ViewSet):
    def get(self, request):
        # get the bearer token from request Authorization header
        # authenticate the user
        user = authenticate(request, token=request.headers.get('Authorization'))
        if user is not None:
            return HttpResponse(f"Hello, {user.username}!", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self, request):
        # get the bearer token from request Authorization header
        # authenticate the user
        user = authenticate(request, token=request.headers.get('Authorization'))
        if user is not None:
            #update the user's last login time
            user.last_login = datetime.now()
            user.save()
            return HttpResponse(f"Last login time updated for {user.username}", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)