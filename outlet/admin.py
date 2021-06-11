from django.contrib import admin
from outlet.models import outlet
# Register your models here.
class OutletAdmin(admin.ModelAdmin):
    search_fields = ["pk","outlet_name"]
    list_display = [
        "pk",
        "outlet_name",
        "outlet_location",
        "outlet_image",
        "is_active",
        "created_at",
        "updated_at",
    ]

admin.site.register(outlet,OutletAdmin)