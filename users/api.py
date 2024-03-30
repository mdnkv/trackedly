from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from users.serializers import (SignupSerializer, UserSerializer, PasswordUpdateSerializer)


class SignupAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PasswordUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
