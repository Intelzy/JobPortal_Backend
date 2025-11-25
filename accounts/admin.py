from django.contrib import admin
from accounts.models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "full_name",
        "company_name",
        "role",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
