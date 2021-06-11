from django.db import models
from accounts.models import custom_user
from outlet.models import outlet
# Create your models here.

class customer(models.Model):
    custom_user_id = models.ForeignKey(custom_user,on_delete=models.CASCADE)
    # outlet_id = models.ForeignKey(outlet, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
