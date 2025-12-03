# https://job-portal-pi-brown.vercel.app/

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema

from accounts.models import CustomUser
from accounts.serializers import UserSerializer, LoginSerializer


# @extend_schema(tags=["Users"])
class UserView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(tags=["Users"])
    def get(self, request, *args, **kwargs):

        if kwargs.get("id"):
            user = get_object_or_404(CustomUser, id=kwargs.get("id"))
            serializer = UserSerializer(user)
        else:
            user = CustomUser.objects.all()
            serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if data.get("role") == "job_seeker":
            data["role"] = "job_seeker"
        elif data.get("role") == "company":
            data["role"] = "company"
        else:
            return Response(
                {"message": "invalid role"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "user created", "payload": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {**serializer.errors, "blabla": "blabla"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(tags=["Users"])
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserSerializer(user)
        user.delete()
        return Response(
            {"payload": serializer.data, "message": "user deleted"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["Users"])
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if not user_id:
            return Response(
                {"message": "user id is not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "data update successfully", "payload": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(tags=["Users"])
    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if not user_id:
            return Response(
                {"message": "user id is not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "data update successfully", "payload": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(tags=["Auth"])
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = UserSerializer(serializer.validated_data["user"])
            return Response(user.data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
