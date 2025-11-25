from django.contrib import admin

# Register your models here.
from company.models import JobModel, ApplicantModel

admin.site.register(JobModel)
admin.site.register(ApplicantModel)
