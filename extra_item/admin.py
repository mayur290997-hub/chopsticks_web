from django.contrib import admin
from extra_item.models import extra_item
# Register your models here.

class extra_itemAdmin(admin.ModelAdmin):
    search_fields = ["pk","order_id"]
    list_display = [
        "pk",
        "extra_item_name",
        "extra_item_price",
        "created_at",
        "updated_at",
    ]
admin.site.register(extra_item,extra_itemAdmin)