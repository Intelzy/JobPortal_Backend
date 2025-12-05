# https://job-portal-pi-brown.vercel.app/

from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema


from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer


class UserView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Users"], request=UserSerializer, responses={200: UserSerializer}
    )
    def get(self, request, *args, **kwargs):

        if kwargs.get("id"):
            user = get_object_or_404(CustomUser, id=kwargs.get("id"))
            serializer = UserSerializer(user)
        else:
            user = CustomUser.objects.all()
            serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Auth"], request=UserSerializer, responses={201: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        if data.get("role") == "jobseeker":
            data["role"] = "jobseeker"
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
        print(serializer.errors)
        return Response(
            {**serializer.errors, "blabla": "blabla"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        tags=["Users"], request=UserSerializer, responses={200: UserSerializer}
    )
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=id)
        serializer = UserSerializer(user)
        user.delete()
        return Response(
            {"payload": serializer.data, "message": "user deleted"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Users"], request=UserSerializer, responses={200: UserSerializer}
    )
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

    @extend_schema(
        tags=["Users"], request=UserSerializer, responses={200: UserSerializer}
    )
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
                {"message": "data updated successfully", "result": serializer.data},
                status=status.HTTP_200_OK,
            )
        print(serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"], request=LoginSerializer, responses={200: LoginSerializer}
    )
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request=request, email=email, password=password)

        if user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Login success", "result": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )
