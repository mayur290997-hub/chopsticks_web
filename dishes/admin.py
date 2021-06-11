from django.contrib import admin
from dishes.models import dishes
# Register your models here.

class dishesAdmin(admin.ModelAdmin):
    search_fields = ["pk","order_id"]
    list_display = [
        "pk",
        "dish_name",
        "quantity",
        "amount",
        "extra_item_1",
        "extra_item_2",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_editable = ["amount", "dish_name","quantity" , ]
admin.site.register(dishes,dishesAdmin)