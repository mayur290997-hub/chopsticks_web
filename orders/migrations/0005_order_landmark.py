# Generated by Django 3.2.4 on 2021-06-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210605_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='landmark',
            field=models.CharField(default='NA', max_length=500),
        ),
    ]
