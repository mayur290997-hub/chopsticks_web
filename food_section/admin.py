from django.contrib import admin
from food_section.models import food_section
# Register your models here.

class food_sectionAdmin(admin.ModelAdmin):
    search_fields = ["pk","order_id"]
    list_display = [
        "pk",
        "section_name",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_editable = ["section_name"]
admin.site.register(food_section,food_sectionAdmin)