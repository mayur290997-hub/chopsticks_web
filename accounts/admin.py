from django.contrib import admin
from accounts.models import custom_user
# Register your models here.
class custom_userAdmin(admin.ModelAdmin):
    search_fields = ["pk","outlet_name"]
    list_display = [
        "pk",
        "mobile_no",
        "otp",
    ]

admin.site.register(custom_user,custom_userAdmin)