from django.contrib import admin

# Register your models here.
from .models import JobModel, ApplicantModel, Skill


class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "company",
        "title",
        "location",
        "salary",
        "type",
        "description",
        "created_at",
        "updated_at",
    ]

    list_filter = ["company"]


class ApplicantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "company",
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


class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(JobModel, JobAdmin)
admin.site.register(ApplicantModel, ApplicantAdmin)
admin.site.register(Skill, SkillAdmin)
