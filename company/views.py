from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from company.models import JobModel, ApplicantModel
from company.serializer import JobSerializer, ApplicantSerializer

# Create your views here.


class JobView(viewsets.ModelViewSet):
    queryset = JobModel.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]


# class JobView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):

#         if kwargs.get("id"):
#             job = get_object_or_404(JobModel, id=kwargs.get("id"))
#             serializer = JobSerializer(job)
#         else:
#             job = JobModel.objects.all()
#             serializer = JobSerializer(job, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = JobSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, *args, **kwargs):
#         job_id = kwargs.get("id")

#         if not job_id:
#             return Response(
#                 {"message": "Job id not provided"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         job = get_object_or_404(JobModel, id=job_id)
#         serializer = JobSerializer(job, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, *arhs, **kwargs):
#         job_id = kwargs.get("id")

#         if not job_id:
#             return Response(
#                 {"message": "Job id not provided"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         job = get_object_or_404(JobModel, id=job_id)
#         serializer = JobSerializer(job, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *arhs, **kwargs):
#         job_id = kwargs.get("id")

#         if not job_id:
#             return Response(
#                 {"message": "Job id not provided"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         job = get_object_or_404(JobModel, id=job_id)
#         serializer = JobSerializer(job)
#         job.delete()
#         return Response(serializer.data, status=status.HTTP_200_OK)
