# Generated by Django 3.2.3 on 2021-05-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.PositiveIntegerField(choices=[(1, 'PENDING'), (2, 'CANCLE'), (3, 'COMPLETE'), (4, 'DELIVERY')]),
        ),
    ]