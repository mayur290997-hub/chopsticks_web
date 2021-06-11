# Generated by Django 3.2.3 on 2021-06-11 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0004_alter_outlet_outlet_image'),
        ('food_section', '0002_food_section_outlet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_section',
            name='outlet_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='outlet.outlet'),
        ),
    ]