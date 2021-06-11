# Generated by Django 3.2.3 on 2021-05-28 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dishes', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.PositiveIntegerField(choices=[(1, 'ONLINE'), (2, 'CASH')])),
                ('order_delivery_address', models.CharField(max_length=50)),
                ('total_bill', models.IntegerField()),
                ('order_status', models.PositiveIntegerField(choices=[(1, 'PENDING'), (2, 'CANCLE'), (3, 'PAID'), (4, 'DELIVERY')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='customer_order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_delivery_address', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dish_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.dishes')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
