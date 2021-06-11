from django.db import models
import datetime,os
# Create your models here.
class outlet(models.Model):
    outlet_name   = models.CharField(max_length=50)
    outlet_location  = models.CharField(max_length=50)
    
    def path_and_rename(self, filename):
        upload_to = 'outlet'
        ext = filename.split('.')[-1]
        if self.username:
            filename = '{}-{}.{}'.format(self.username, datetime.date.today(), ext)

        return os.path.join(upload_to, filename)

    outlet_image   = models.ImageField(upload_to='path_and_rename', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)