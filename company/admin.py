from django.contrib import admin

# Register your models here.
from company.models import JobModel, ApplicantModel, Skill


class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "title",
        "role",
        "salary",
        "location",
        "description",
        "time",
        "type",
        "created_at",
        "updated_at",
    ]


class ApplicantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "job",
        "name",
        "email",
        "role",
        "experience",
        "status",
    ]


admin.site.register(JobModel, JobAdmin)
admin.site.register(ApplicantModel, ApplicantAdmin)
admin.site.register(Skill)
