from django.db import models
from outlet.models import outlet

# Create your models here.
class food_section(models.Model):
    section_name = models.CharField(max_length=50)
    outlet_id = models.ForeignKey(outlet,on_delete=models.CASCADE,default=1)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
