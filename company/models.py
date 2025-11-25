from django.db import models

from accounts.models import CustomUser


class JobTime(models.TextChoices):
    REMOTE = "remote", "Remote"
    PHYSICAL = "physical", "Physical"


class JobType(models.TextChoices):
    PART_TIME = "part_time", "Part Time"
    FULL_TIME = "full_time", "Full Time"


class JobStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    REVIEWED = "reviewed", "Reviewed"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


# Create your models here.
class JobModel(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    salary = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True, null=True)
    time = models.CharField(
        max_length=20, choices=JobTime.choices, default=JobTime.PHYSICAL
    )
    type = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.FULL_TIME
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApplicantModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    experience = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=JobStatus.choices, default=JobStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
