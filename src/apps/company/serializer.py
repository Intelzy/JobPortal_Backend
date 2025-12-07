from django.shortcuts import get_object_or_404

from rest_framework import serializers

from src.apps.accounts.serializers import UserSerializer
from .models import JobModel, ApplicantModel, JobRequirement
from src.apps.accounts.models import CustomUser


class ApplicantMiniSerlaizer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ApplicantModel
        fields = [
            "id",
            "full_name",
            "email",
            "contact",
            "experience",
            "status",
            "portfolio_url",
            "linkedin_url",
            "created_at",
            "updated_at",
        ]


class JobMiniSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = JobModel
        fields = [
            "id",
            "company",
            "title",
            "location",
            "salary",
            "requirements",
            "type",
            "description",
            "created_at",
            "updated_at",
        ]


class JobSerializer(serializers.ModelSerializer):

    applicants = serializers.SerializerMethodField(read_only=True)

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
            "applicants",
        ]

    def get_applicants(self, obj):
        request = self.context.get("request")

        return ApplicantMiniSerlaizer(
            obj.applicants.all(), many=True, context={"request": request}
        ).data

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

    job_id = serializers.IntegerField(required=True, write_only=True)
    job = JobMiniSerializer(read_only=True)

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    cv_url = serializers.SerializerMethodField(read_only=True)
    cover_letter_url = serializers.SerializerMethodField(read_only=True)

    cv = serializers.FileField(required=False, allow_null=True, write_only=True)
    cover_letter = serializers.FileField(
        required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = ApplicantModel
        fields = [
            "user_id",
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
            "cv_url",
            "cover_letter_url",
            "created_at",
            "updated_at",
        ]

    def get_cv_url(self, obj):
        request = self.context.get("request")
        if obj.cv and request:
            return request.build_absolute_uri(obj.cv.url)
        return None

    def get_cover_letter_url(self, obj):
        request = self.context.get("request")
        if obj.cover_letter and request:
            return request.build_absolute_uri(obj.cover_letter.url)
        return None

    def create(self, validated_data):
        job_id = validated_data.pop("job_id")
        job = get_object_or_404(JobModel, id=job_id)

        validated_data["company"] = job.company
        validated_data["job"] = job

        applicant = ApplicantModel.objects.create(**validated_data)
        return applicant
