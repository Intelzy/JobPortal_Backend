from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from company.models import JobModel, ApplicantModel
from company.serializer import JobSerializer, ApplicantSerializer, ProfileSerializer
from accounts.models import CustomUser
from accounts.serializers import UserSerializer

# Create your views here.


@extend_schema(
    tags=["Users"], request=ApplicantSerializer, responses={200: ApplicantSerializer}
)
class ApplicantView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Applicant"])
    def get(self, request, *args, **kwargs):

        id = kwargs.get("id")
        job_id = request.params.get("job_id")
        company_id = request.params.get("company_id")
        applicant_status = request.params.get("status")
        applicants = ApplicantModel.objects.all()

        if job_id:
            applicants = applicants.filter(status=applicant_status)
        if company_id:
            applicants = applicants.filter(company_id=company_id)
        if id:
            applicants = get_object_or_404(ApplicantModel, id=id)
            serializer = ApplicantSerializer(applicants)
        return Response(
            {"result": serializer.data, "count": applicants.count()},
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["Applicant"])
    def post(self, request, *args, **kwargs):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Applicant"])
    def put(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicants = get_object_or_404(ApplicantModel, id=id)
        serializer = ApplicantSerializer(applicants, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Applicant"])
    def patch(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicants = get_object_or_404(ApplicantModel, id=id)
        serializer = ApplicantSerializer(applicants, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Applicant"])
    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(ApplicantModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Users"], request=JobSerializer, responses={200: JobSerializer})
class JobView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Job"])
    def get(self, request, *args, **kwargs):

        company_id = kwargs.get("company_id")

        if company_id:
            company = get_object_or_404(CustomUser, id=company_id)
            jobs = company.jobs.all()
            serializer = JobSerializer(jobs, many=True)
            return Response(
                {"result": serializer.data, "count": jobs.count()},
                status=status.HTTP_200_OK,
            )

        id = kwargs.get("id")
        if id:
            jobs = get_object_or_404(JobModel, id=id)
            serializer = JobSerializer(jobs)
            applicant_count = jobs.applicants.all().count()

            return Response(
                {"result": serializer.data, "applicant_count": applicant_count},
                status.HTTP_200_OK,
            )

        jobs = JobModel.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(
            {
                "result": serializer.data,
                "count": jobs.count(),
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["Job"])
    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Job"])
    def put(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        jobs = get_object_or_404(JobModel, id=id)
        serializer = JobSerializer(jobs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Job"])
    def patch(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        jobs = get_object_or_404(JobModel, id=id)
        serializer = JobSerializer(jobs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Job"])
    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(JobModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Profile"], request=ProfileSerializer, responses={200: ProfileSerializer}
)
class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        id = kwargs.get("company_id")
        if not id:
            return Response(
                {"message": "Id not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        company = get_object_or_404(CustomUser, id=id)
        comany_data = UserSerializer(company)
        job = company.jobs.all()
        job_data = JobSerializer(job, many=True)
        applicant = company.applicants.all()
        applicant_data = ApplicantSerializer(applicant, many=True)
        return Response(
            {
                "comany_data": comany_data.data,
                "job_data": job_data.data,
                "job_count": job.count(),
                "applicant_data": applicant_data.data,
                "applicant_count": applicant.count(),
            },
            status=status.HTTP_200_OK,
        )
