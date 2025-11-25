from rest_framework import serializers

from accounts.serializers import UserSerializer
from company.models import JobModel, ApplicantModel


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = JobModel
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ApplicantModel
        fields = "__all__"
