from django.db import models
from src.apps.accounts.models import CustomUser


class JobType(models.TextChoices):
    FULL_TIME = "Full-time", "Full-time"
    PART_TIME = "Part-time", "Part-time"
    CONTRACT = "Contract", "Contract"
    INTERNSHIP = "Internship", "Internship"


class JobStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    REVIEWED = "reviewed", "Reviewed"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobRequirement(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class JobModel(models.Model):

    company = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    salary = models.IntegerField()
    type = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.FULL_TIME
    )
    description = models.CharField(max_length=1000, blank=True, null=True)
    # skills = models.ManyToManyField(Skill, related_name="skill")

    requirements = models.ManyToManyField(
        JobRequirement, blank=True, related_name="requirements"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ApplicantModel(models.Model):
    company = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="applicants"
    )
    job = models.ForeignKey(
        JobModel, on_delete=models.CASCADE, related_name="applicants"
    )
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField()
    experience = models.IntegerField()
    status = models.CharField(choices=JobStatus, default=JobStatus.PENDING)
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to="cv/", blank=True, null=True)
    cover_letter = models.FileField(upload_to="cover_letter/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
