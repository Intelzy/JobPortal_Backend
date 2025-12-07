from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter

from src.apps.company.models import JobModel, ApplicantModel
from src.apps.company.models import JobModel, ApplicantModel
from src.apps.company.serializer import JobSerializer, ApplicantSerializer

from src.apps.accounts.models import CustomUser
from src.apps.accounts.serializers import UserSerializer


# Create your views here.
class ApplicantView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Applicant"],
        request=ApplicantSerializer,
        responses={200: ApplicantSerializer},
        parameters=[
            OpenApiParameter(
                name="status",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by applicant status",
            ),
            OpenApiParameter(
                name="job_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter by job id",
            ),
            OpenApiParameter(
                name="company_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter by company_id",
            ),
            OpenApiParameter(
                name="user_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter by user id",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):

        id = kwargs.get("id")
        if id:
            applicants = get_object_or_404(ApplicantModel, id=id)
            serializer = ApplicantSerializer(applicants, context={"request": request})
            return Response(
                {"result": serializer.data},
                status=status.HTTP_200_OK,
            )

        user_id = request.query_params.get("user_id")
        job_id = request.query_params.get("job_id")
        company_id = request.query_params.get("company_id")
        applicant_status = request.query_params.get("status")

        applicants = ApplicantModel.objects.all()

        if user_id:
            applicants = applicants.filter(user_id=user_id)
        if applicant_status:
            applicants = applicants.filter(status=applicant_status)
        if job_id:
            applicants = applicants.filter(job_id=job_id)
        if company_id:
            applicants = applicants.filter(company_id=company_id)

        serializer = ApplicantSerializer(
            applicants, many=True, context={"request": request}
        )
        return Response(
            {"result": serializer.data, "count": applicants.count()},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Applicant"],
        request=ApplicantSerializer,
        responses={201: ApplicantSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = ApplicantSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Applicant"],
        request=ApplicantSerializer,
        responses={200: ApplicantSerializer},
    )
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

    @extend_schema(
        tags=["Applicant"],
        request=ApplicantSerializer,
        responses={200: ApplicantSerializer},
    )
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

    @extend_schema(
        tags=["Applicant"],
        request=ApplicantSerializer,
        responses={200: ApplicantSerializer},
    )
    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(ApplicantModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)


class JobView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Job"],
        request=JobSerializer,
        responses={200: JobSerializer},
        parameters=[
            OpenApiParameter(
                name="company_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter by company id",
            )
        ],
    )
    def get(self, request, *args, **kwargs):

        company_id = request.query_params.get("company_id")
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

            return Response(
                {"result": serializer.data},
                status.HTTP_200_OK,
            )

        jobs = JobModel.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(
            {"result": serializer.data, "count": jobs.count()},
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["Job"], request=JobSerializer, responses={201: JobSerializer})
    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Job"], request=JobSerializer, responses={200: JobSerializer})
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

    @extend_schema(tags=["Job"], request=JobSerializer, responses={200: JobSerializer})
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

    @extend_schema(tags=["Job"], request=JobSerializer, responses={200: JobSerializer})
    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        if not id:
            return Response(
                {"message": "id required"}, status=status.HTTP_400_BAD_REQUEST
            )
        applicant = get_object_or_404(JobModel, id=id)
        applicant.delete()
        return Response({"message": "applicant deleted"}, status=status.HTTP_200_OK)


# class ProfileView(APIView):
#     permission_classes = [AllowAny]

#     @extend_schema(
#         tags=["Profile"], request=ProfileSerializer, responses={200: ProfileSerializer}
#     )
#     def get(self, request, *args, **kwargs):
#         id = kwargs.get("company_id")
#         if not id:
#             return Response(
#                 {"message": "Id not found"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         company = get_object_or_404(CustomUser, id=id)
#         comany_data = UserSerializer(company)
#         job = company.jobs.all()
#         job_data = JobSerializer(job, many=True)
#         applicant = company.applicants.all()
#         applicant_data = ApplicantSerializer(applicant, many=True)
#         return Response(
#             {
#                 "comany_data": comany_data.data,
#                 "job_data": job_data.data,
#                 "job_count": job.count(),
#                 "applicant_data": applicant_data.data,
#                 "applicant_count": applicant.count(),
#             },
#             status=status.HTTP_200_OK,
#         )
