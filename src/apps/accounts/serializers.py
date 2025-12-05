from rest_framework import serializers
from django.contrib.auth import authenticate, login

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "role",
            "full_name",
            "company_name",
            "password1",
            "password2",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Password must match")
        if len(attrs["password1"]) < 8:
            raise serializers.ValidationError(
                "Password is too short. Use at least 8 character"
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserSerializer
        fields = ["email", "password"]
