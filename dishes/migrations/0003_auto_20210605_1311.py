# Generated by Django 3.2.4 on 2021-06-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0002_dishes_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishes',
            name='extra_item_cost_1',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='dishes',
            name='extra_item_cost_2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='dish_type',
            field=models.PositiveIntegerField(choices=[(1, 'VEG'), (2, 'NON_VEG'), (3, 'none')]),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='extra_item_1',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='extra_item_2',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
