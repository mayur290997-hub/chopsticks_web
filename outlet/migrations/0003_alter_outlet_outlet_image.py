# Generated by Django 3.2.3 on 2021-06-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0002_alter_outlet_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='outlet_image',
            field=models.FileField(blank=True, upload_to='outlet'),
        ),
    ]
