from django.contrib import admin
from customer.models import customer
# from import_export.admin import ImportExportModelAdmin
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["pk","full_name"]
    list_display = [
        "pk",
        "full_name",
        "address",
        "created_at",
        "updated_at",
    ]
    # list_editable = ["full_name", "address" ]
admin.site.register(customer,CustomerAdmin)
