# Generated by Django 3.2.3 on 2021-06-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
