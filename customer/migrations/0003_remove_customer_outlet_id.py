# Generated by Django 3.2.3 on 2021-06-11 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_outlet_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='outlet_id',
        ),
    ]
