from django.db import models
from food_section.models import food_section
from extra_item.models import extra_item
# Create your models here.

class dishes(models.Model):
    food_section_id = models.ForeignKey(food_section,on_delete=models.CASCADE)
    VEG = 1
    NON_VEG = 2
    none = 3
    ROLE_CHOICES = (
      (VEG,'VEG'),
      (NON_VEG,'NON_VEG'),
      (none,'none'),
    )
    dish_type = models.PositiveIntegerField(choices=ROLE_CHOICES)
    dish_name = models.CharField(max_length=50)
    quantity  = models.IntegerField()
    amount = models.IntegerField()
    extra_item_1  = models.CharField(max_length=500,blank=True)
    extra_item_cost_1 = models.IntegerField(blank=True,default=0,null=True)
    extra_item_2  = models.CharField(max_length=500,blank=True)
    extra_item_cost_2 = models.IntegerField(blank=True,default=0,null=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
