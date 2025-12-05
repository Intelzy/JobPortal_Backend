from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accounts.serializers import UserSerializer
from company.models import JobModel, ApplicantModel, Skill, JobRequirement
from accounts.models import CustomUser


class JobSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(required=True)
    company = UserSerializer(read_only=True)

    requirements_input = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    requirements = serializers.SerializerMethodField(read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = JobModel
        fields = [
            "id",
            "company_id",
            "company",
            "title",
            "location",
            "salary",
            "requirements",
            "requirements_input",
            "type",
            "description",
            "created_at",
            "updated_at",
        ]

    def get_requirements(self, obj):
        return [r.name for r in obj.requirements.all()]

    def validate(self, attrs):
        user = get_object_or_404(CustomUser, id=attrs.get("company_id"))
        if user.role != "company":
            raise serializers.ValidationError("Only company can post the job")
        return attrs

    def create(self, validated_data):
        req_list = validated_data.pop("requirements_input", [])
        company_id = validated_data.pop("company_id")
        company = get_object_or_404(CustomUser, id=company_id)
        validated_data["company"] = company
        # create job without M2M
        job = JobModel.objects.create(**validated_data)

        # attach requirements
        for r in req_list:
            req_obj, _ = JobRequirement.objects.get_or_create(name=r)
            job.requirements.add(req_obj)

        return job


class ApplicantSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(required=True)

    job = JobSerializer(read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ApplicantModel
        fields = [
            "id",
            "job_id",
            "job",
            "full_name",
            "email",
            "contact",
            "experience",
            "status",
            "portfolio_url",
            "linkedin_url",
            "cv",
            "cover_letter",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        job_id = validated_data.pop("job_id")
        job = get_object_or_404(JobModel, id=job_id)

        validated_data["company"] = job.company
        validated_data["job"] = job

        appplicant = ApplicantModel.objects.create(**validated_data)
        return appplicant


class ProfileSerializer(serializers.Serializer):
    company = UserSerializer()
    jobs = JobSerializer()
    applicants = ApplicantSerializer()

    class Model:
        fields = ["company", "jobs", "applicants"]
