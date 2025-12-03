from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema


from company.models import JobModel, ApplicantModel
from company.serializer import (
    JobSerializer,
    ApplicantSerializer,
)

# Create your views here.


@extend_schema(tags=["Applicants"])
class ApplicantView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if id:
            applicants = get_object_or_404(ApplicantModel, id=id)
            serializer = ApplicantSerializer(applicants)
            return Response(serializer.data, status.HTTP_200_OK)

        applicant_status = kwargs.get("status")
        if applicant_status:
            applicants = ApplicantModel.objects.filter(status=applicant_status)
            serializer = ApplicantSerializer(applicants, many=True)
            return Response(
                {"payload": serializer.data, "count": applicants.count()},
                status=status.HTTP_200_OK,
            )

        applicants = ApplicantModel.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(
            {"payload": serializer.data, "count": applicants.count()},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(ApplicantModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Jobs"])
class JobView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if id:
            jobs = get_object_or_404(JobModel, id=id)
            serializer = JobSerializer(jobs)
            return Response(serializer.data, status.HTTP_200_OK)

        jobs = JobModel.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(
            {"payload": serializer.data, "count": jobs.count()},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(JobModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)
