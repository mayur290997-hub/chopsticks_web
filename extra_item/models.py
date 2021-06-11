from django.db import models
# Create your models here.

class extra_item(models.Model):
    extra_item_name = models.CharField(max_length=50)
    extra_item_price  = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
