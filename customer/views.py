from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from customer.models import customer
from accounts.models import custom_user
from orders.models import order,customer_order_detail
from dishes.models import dishes
from food_section.models import food_section
from outlet.models import outlet
import math
# Create your views here.

@login_required(login_url = '/accounts/user_login')
def customer_master(request):
    user = request.user
    # outlet_objects = outlet.objects.get(pk=pk)
    all_customer = customer.objects.all()
    all_user= customer.objects.all().count()
    location = outlet.objects.all().filter(is_active=True)
    total_billing = {}
    last_order = {}
    for one in all_customer :
        sum = 0
        if order.objects.filter(customer_id=one).exists():
            last_order[one.pk] = order.objects.filter(customer_id=one).latest('created_at').created_at
            order_object = order.objects.filter(customer_id=one)

            for two in order_object:
                sum = sum + two.total_bill
                total_billing[one.pk]=sum
        else:
            total_billing[one.pk] = 'NO ORDERS'
            last_order [one.pk] = 'NO ORDERS'
    food_objects = food_section.objects.all().first()
    if request.method == "POST":
        last_date = request.POST['last_date']
        last_orders = order.objects.filter(created_at__date=last_date)
        for one in all_customer :
            sum = 0
            if order.objects.filter(customer_id=one,created_at__date=last_date).exists():
                last_order[one.pk] = order.objects.filter(customer_id=one,created_at__date=last_date).latest('created_at').created_at
                order_object = order.objects.filter(customer_id=one)

                for two in order_object:
                    sum = sum + two.total_bill
                    total_billing[one.pk]=sum
            else:
                total_billing[one.pk] = 'NO ORDERS'
                last_order [one.pk] = 'NO ORDERS'
        data = {'all_customer':all_customer,'all_user':all_user,'total_billing':total_billing,'last_order':last_order,'food_objects':food_objects,'last_date':last_date,'location':location}
        return render(request, 'customer/customer.html',data)
    else:
        data = {'all_customer':all_customer,'all_user':all_user,'total_billing':total_billing,'last_order':last_order,'food_objects':food_objects,'location':location}
        return render(request, 'customer/customer.html',data)

@login_required(login_url = '/accounts/user_login')
def update_customer(request,pk,pk1):
    user = request.user
    outlet_objects = outlet.objects.get(pk=pk)
    all_customer = customer.objects.get(pk=pk1)
    location = outlet.objects.all().filter(is_active=True)
    if request.method == "POST":
        full_name= request.POST['full_name']
        mobile_no= request.POST['mobile_no']
        email=request.POST['email']
        address= request.POST['address']
        all_customer.full_name=full_name
        all_customer.mobile_no=mobile_no
        all_customer.email=email
        all_customer.address=address
        all_customer.save()
        return HttpResponseRedirect(reverse('customer:customer_detail',kwargs={'pk':outlet_objects.pk,'pk1':all_customer.pk}))

# email = custom_user.objects.get(pk=request.POST['email'])

@login_required(login_url = '/accounts/user_login')
def customer_detail(request,pk,pk1):
    user= request.user
    outlet_objects = outlet.objects.get(pk=pk)
    all_customer = customer.objects.get(pk=pk1)
    order_details = order.objects.filter(customer_id=all_customer,outlet_id=outlet_objects)
    total_order_count=order_details.filter(outlet_id=outlet_objects).count()
    total_order_cancle=order_details.filter(order_status=2,outlet_id=outlet_objects).count()
    latest_order = order_details.all()
    customer_details = customer_order_detail.objects.filter(order_id=latest_order)
    location = outlet.objects.all().filter(is_active=True)
    error_msg = 'NO Order'
    error_massage = 'NO Order'

    sum = 0
    for one in order_details :
        sum = sum + one.total_bill
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data = {'all_customer':all_customer,'order_details':order_details,'total_order_count':total_order_count,
            'total_order_cancle':total_order_cancle,'sum':sum,'error_msg':error_msg,'latest_order':latest_order,
            'customer_details':customer_details,'food_objects':food_objects,'location':location,'outlet_objects':outlet_objects}
    return render (request,'customer/customer_detail.html',data)



@login_required(login_url = '/accounts/user_login')
def delete_order(request,pk,pk1):
    outlet_objects = outlet.objects.get(pk=pk)
    order_object = customer_order_detail.objects.get(pk=pk1)
    order_object.delete()
    return HttpResponseRedirect(reverse('customer:customer_master',kwargs={'pk':outlet_objects.pk}))
