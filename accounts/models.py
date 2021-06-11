from django.db import models
import datetime
import os
from django.contrib.auth.models import AbstractUser
# Create your models here.

class custom_user(AbstractUser):
    SUPER_ADMIN = 1
    ADMIN = 2
    CUSTOMER = 3
    ROLE_CHOICES = (
      (SUPER_ADMIN,'Super Admin'),
      (ADMIN,'Admin'),
      (CUSTOMER,'CUSTOMER'),
    )
    mobile_no  = models.CharField(max_length=50)
    user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=ADMIN)
    otp = models.IntegerField(default=0)
    Updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)