from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accounts.serializers import UserSerializer
from company.models import JobModel, ApplicantModel
from accounts.models import CustomUser


class JobSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = JobModel
        fields = [
            "user_id",
            "title",
            "role",
            "salary",
            "location",
            "description",
            "time",
            "type",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        validated_data["user"] = user
        job = JobModel.objects.create(**validated_data)
        return job


class ApplicantSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    job_id = serializers.IntegerField(required=True)

    class Meta:
        model = ApplicantModel
        fields = [
            "user_id",
            "job_id",
            "id",
            "name",
            "email",
            "role",
            "experience",
            "status",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        job_id = validated_data.pop("job_id")

        user = get_object_or_404(CustomUser, id=user_id)
        job = get_object_or_404(JobModel, id=job_id)

        validated_data["user"] = user
        validated_data["job"] = job

        applicant = ApplicantModel.objects.create(**validated_data)
        return applicant
