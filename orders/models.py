from django.db import models

from customer.models import customer
from extra_item.models import extra_item
from dishes.models import dishes
from outlet.models import outlet
# Create your models here.

class order(models.Model):
    order_id = models.CharField(max_length=50)
    customer_id  = models.ForeignKey(customer,on_delete=models.CASCADE)
    outlet_id = models.ForeignKey(outlet, on_delete=models.CASCADE)
    ONLINE = 1
    CASH =2
    PAYMENT_TYPE_CHOICES = (
      (ONLINE,'ONLINE'),
      (CASH,'CASH'),
    )
    payment_type  = models.PositiveIntegerField(choices=PAYMENT_TYPE_CHOICES)
    order_delivery_address = models.CharField(max_length=500)
    landmark = models.CharField(max_length=500,default="NA")
    total_bill  = models.IntegerField()

    PENDING= 1
    CANCLE = 2
    COMPLETE = 3
    DELIVERY = 4
    ORDER_STATUS_CHOICES = (
      (PENDING,'PENDING'),
      (CANCLE,'CANCLE'),
      (COMPLETE,'COMPLETE'),
      (DELIVERY,'DELIVERY'),
    )
    order_status = models.PositiveIntegerField(choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class customer_order_detail(models.Model):
    order_id   = models.ForeignKey(order,on_delete=models.CASCADE)
    dish_id  = models.ForeignKey(dishes,on_delete=models.CASCADE)
    quantity   = models.IntegerField()
    amount    = models.IntegerField()
    extra_item_1 = models.BooleanField(default=False)
    extra_item_2 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)