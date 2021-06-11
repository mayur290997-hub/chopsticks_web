from django.contrib import admin
from orders.models import order,customer_order_detail
# Register your models here.

class orderAdmin(admin.ModelAdmin):
    search_fields = ["pk","order_id"]
    list_display = [
        "pk",
        "order_id",
        "payment_type",
        "order_delivery_address",
        "total_bill",
        "order_status",
        "created_at",
        "updated_at",
    ]

class customer_order_detailAdmin(admin.ModelAdmin):
    search_fields = ["pk","order_id"]
    list_display = [
        "pk",
        "order_id",
        "dish_id",
        "quantity",
        "amount",
        "created_at",
        "updated_at",
    ]

admin.site.register(order,orderAdmin)
admin.site.register(customer_order_detail,customer_order_detailAdmin)