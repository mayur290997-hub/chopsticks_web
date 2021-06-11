from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta,datetime
from django.http import JsonResponse

from orders.models import order,customer_order_detail
from customer.models import customer
from accounts.models import custom_user
from food_section.models import food_section
from dishes.models import dishes
from outlet.models import outlet
from django.utils.datastructures import MultiValueDictKeyError
import random
# Create your views here.

def select_order_item(request,pk):
    outlet_objects = outlet.objects.get(pk=pk)
    all_dishes =  dishes.objects.filter(is_active=True,food_section_id__outlet_id=outlet_objects).all()
    if request.method == "POST":
        selected_dish = []
        not_selected = []
        for one_dish in all_dishes:
            try:
                dish = dishes.objects.get(pk=request.POST['dish'+ str(one_dish.pk)])
            except MultiValueDictKeyError:
                dish = " "

            quantity = request.POST['quantity' + str(one_dish.pk)]

            try:
                extra_item1 = request.POST['extra_item1' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item1 = "0"

            try:
                extra_item2 = request.POST['extra_item2' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item2 = "0"

            if dish != " ":
                selected_dish.append([dish,quantity,extra_item1,extra_item2])
            else:
                not_selected.append([dish,quantity,extra_item1,extra_item2])
        total_amount = 0
        total_quantity = 0
        for item in selected_dish:
            total_quantity = total_quantity + int(item[1])

            if item[2] == "1":
                extra_item1_cost = item[0].extra_item_cost_1
            else:
                extra_item1_cost = 0

            if item[3] == "1":
                extra_item2_cost = item[0].extra_item_cost_2
            else:
                extra_item2_cost = 0

            total_amount = total_amount + (int(item[0].amount) * int(item[1])) + int(extra_item1_cost) + int(extra_item2_cost)

        data = {'selected_dish':selected_dish,'total_quantity':total_quantity,'total_amount':total_amount,'outlet_objects':outlet_objects}
        return render(request,'orders/order_cart.html',data)



def order_placed(request,pk):
    outlet_objects = outlet.objects.get(pk=pk)
    all_dishes =  dishes.objects.filter(is_active=True).all()
    if request.method == "POST":
        selected_dish = []
        not_selected = []
        for one_dish in all_dishes:
            try:
                dish = dishes.objects.get(pk=request.POST['dish'+ str(one_dish.pk)])
            except MultiValueDictKeyError:
                dish = "0"

            try:
                quantity = request.POST['quantity' + str(one_dish.pk)]
                if quantity != "0":
                    quantity = quantity
                else:
                    quantity = "0"
            except MultiValueDictKeyError:
                quantity = "0"

            try:
                extra_item1 = request.POST['extra_item1' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item1 = "0"

            try:
                extra_item2 = request.POST['extra_item2' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item2 = "0"

            if dish != "0":
                selected_dish.append([dish,quantity,extra_item1,extra_item2])
            else:
                not_selected.append([dish,quantity,extra_item1,extra_item2])

        user_name = request.POST['user_name']
        user_mobile = request.POST['user_mobile']
        user_address = request.POST['user_address']
        landmark = request.POST['landmark']
        payment = request.POST['payment']
        if payment == "1":
            pay = 1
        else:
            pay = 2
        if custom_user.objects.filter(username =user_mobile).exists():
            customuser_obj = custom_user.objects.get(username =user_mobile)
            customer_obj = customer.objects.get(custom_user_id=customuser_obj)
            number = random.randint(1000, 9999)
            customuser_obj.otp = number
            customuser_obj.save()
        else:
            number = random.randint(1000, 9999)
            customuser_obj = custom_user.objects.create(username=user_mobile,
                                                        mobile_no=user_mobile,
                                                        password=make_password(user_mobile),
                                                        user_role=3,
                                                        otp=number)
            customer_obj = customer.objects.create(custom_user_id=customuser_obj,
                                                full_name=user_name,
                                                address=user_address)
        total_amount = 0
        for item in selected_dish:
            if item[2] == "1":
                extra_item1_cost = item[0].extra_item_cost_1
            else:
                extra_item1_cost = 0

            if item[3] == "1":
                extra_item2_cost = item[0].extra_item_cost_2
            else:
                extra_item2_cost = 0

            total_amount = total_amount + (int(item[0].amount) * int(item[1])) + int(extra_item1_cost) + int(extra_item2_cost)

        todays_date = date.today()
        order_id = str(customuser_obj.username[:4]) + "/" + str(todays_date.day) + "" + str(todays_date.month) + "/" + str(todays_date.year)
        order_obj = order.objects.create(order_id=order_id,
                                        outlet_id = outlet_objects,
                                        customer_id=customer_obj,
                                        payment_type=pay,
                                        order_delivery_address=user_address,
                                        landmark=landmark,
                                        total_bill=total_amount,
                                        order_status=1)
        for one_selected in selected_dish:
            if one_selected[2] == "1":
                extra_item_1 = True
                cost_extra1 = one_selected[0].extra_item_cost_1
            else:
                extra_item_1 = False
                cost_extra1 = 0

            if one_selected[3] == "1":
                extra_item_2 = True
                cost_extra2 = one_selected[0].extra_item_cost_2
            else:
                extra_item_2 = False
                cost_extra2 = 0
            one_amount = int(one_selected[1]) * int(one_selected[0].amount) + int(cost_extra1) + int(cost_extra2)
            customer_order_detail.objects.create(order_id=order_obj,
                                                dish_id=one_selected[0],
                                                quantity=one_selected[1],
                                                amount=one_amount,
                                                extra_item_1=extra_item_1,
                                                extra_item_2=extra_item_2)
        return HttpResponseRedirect(reverse('orders:success_order',kwargs={'pk':outlet_objects.pk}))


def success_order(request,pk):
    outlet_objects = outlet.objects.get(pk=pk)
    data = {'outlet_objects':outlet_objects}
    return render(request,'orders/order_success.html',data)


@login_required(login_url = '/accounts/web_login')
def cust_order_details(request):
    user = request.user
    location = outlet.objects.all().filter(is_active=True)
    all_customer = customer.objects.get(custom_user_id=user)
    order_details = order.objects.filter(customer_id=all_customer).all()
    customer_details = customer_order_detail.objects.filter(order_id=order_details)
    data ={'all_customer':all_customer,'order_details':order_details,'customer_details':customer_details,'location':location}
    return render (request,'orders/cust_order_detail.html',data)

@login_required(login_url = '/accounts/user_login')
def order_master(request,pk):
    user= request.user
    location = outlet.objects.all().filter(is_active=True)
    outlet_objects = outlet.objects.get(pk=pk)
    all_orders = order.objects.all().exclude(order_status = 2).filter(outlet_id=outlet_objects)
    total_complete = order.objects.filter(order_status = 3).count()
    total_pending = order.objects.filter(order_status = 1).count()
    total_cancle = order.objects.filter(order_status = 2).count()
    item_count = {}
    sum = 0
    for one in all_orders:
        sum = sum + one.total_bill
        if customer_order_detail.objects.filter(order_id=one).exists():
            item_count[one.pk] = customer_order_detail.objects.filter(order_id=one).count()
        else:
            item_count[one.pk] = 0
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data = {'all_orders':all_orders,'total_complete':total_complete,'total_pending':total_pending,'total_cancle':total_cancle,
    'food_objects':food_objects,'item_count':item_count,'sum':sum,'outlet_objects':outlet_objects,'location':location}
    return render(request,'orders/orders.html',data)


@login_required(login_url = '/accounts/user_login')
def today_order(request,pk):
    user= request.user
    outlet_objects = outlet.objects.get(pk=pk)
    location = outlet.objects.all().filter(is_active=True)
    todays_date = date.today()
    all_orders = order.objects.filter(created_at__date=todays_date,outlet_id=outlet_objects).all()
    total_complete = order.objects.filter(order_status = 3,created_at__date=todays_date).count()
    total_pending = order.objects.filter(order_status = 1,created_at__date=todays_date).count()
    total_cancle = order.objects.filter(order_status = 2,created_at__date=todays_date).count()
    item_count = {}
    sum = 0
    for one in all_orders:
        sum = sum + one.total_bill
        if customer_order_detail.objects.filter(order_id=one).exists():
            item_count[one.pk] = customer_order_detail.objects.filter(order_id=one).count()
        else:
            item_count[one.pk] = 0
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data = {'all_orders':all_orders,'total_complete':total_complete,'total_pending':total_pending,'total_cancle':total_cancle,
    'food_objects':food_objects,'item_count':item_count,'sum':sum,'outlet_objects':outlet_objects,'location':location}
    return render(request,'orders/todays_order.html',data)


@login_required(login_url = '/accounts/user_login')
def order_cancle(request,pk):
    user= request.user
    location = outlet.objects.all().filter(is_active=True)
    outlet_objects = outlet.objects.get(pk=pk)
    all_orders = order.objects.all().filter(order_status=2,outlet_id=outlet_objects)
    item_count = {}
    for one in all_orders:
        if customer_order_detail.objects.filter(order_id=one).exists():
            item_count[one.pk] = customer_order_detail.objects.filter(order_id=one).count()
        else:
            item_count[one.pk] = 0
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data = {'all_orders':all_orders,'food_objects':food_objects,'item_count':item_count,'outlet_objects':outlet_objects,'location':location}
    return render(request,'orders/cancle_order.html',data)


@login_required(login_url = '/accounts/user_login')
def update_status(request,pk,pk1):
    all_order = order.objects.get(pk=pk1)
    outlet_objects = outlet.objects.get(pk=pk)
    if request.method == "POST":
        order_status = request.POST['order_status']
        all_order.order_status=order_status
        all_order.save()
        return HttpResponseRedirect(reverse('orders:order_master',kwargs={'pk':outlet_objects.pk}))


@login_required(login_url = '/accounts/user_login')
def new_order(request,pk):
    user = request.user
    outlet_objects = outlet.objects.get(pk=pk)
    all_food_section = food_section.objects.all().filter(is_active=True,outlet_id=outlet_objects)
    all_customers = custom_user.objects.all().filter(user_role=3)
    all_dishes = dishes.objects.all().filter(is_active=True,food_section_id__outlet_id=outlet_objects)
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data = {'all_customers':all_customers,'all_food_section':all_food_section,'all_dishes':all_dishes,'food_objects':food_objects,'outlet_objects':outlet_objects}
    return render(request,'orders/new_order.html',data)


@login_required(login_url = '/accounts/user_login')
def get_customer_detail(request):
    mobile_num = request.GET.get('mobile_num', None)
    if custom_user.objects.filter(username = mobile_num).exists():
        custom_user_obj = custom_user.objects.get(username = mobile_num)
        customer_obj = customer.objects.get(custom_user_id=custom_user_obj)
        order_details = order.objects.filter(customer_id=customer_obj)
        total_sum = 0
        for one in order_details:
            total_sum = total_sum + int(one.total_bill)
        is_user = 1
        user_mobile = custom_user_obj.username
        user_name = customer_obj.full_name
        user_address = customer_obj.address
        total_order_count = order_details.count()
        total_order_cancle = order_details.filter(order_status=2).count()
    else:
        is_user = 0
        user_mobile = ""
        user_name = ""
        user_address = ""
        total_order_count = "0"
        total_order_cancle = "0"
        total_sum = 0
    data ={'is_user':is_user,'user_mobile':user_mobile,'user_name':user_name,'user_address':user_address,
            'total_order_count':total_order_count,'total_order_cancle':total_order_cancle,'total_sum':total_sum}
    return JsonResponse(data)



@login_required(login_url = '/accounts/user_login')
def order_details(request,pk,pk1):
    outlet_objects = outlet.objects.get(pk=pk)
    order_details = order.objects.get(pk=pk1)
    location = outlet.objects.all().filter(is_active=True)
    all_orders_details = customer_order_detail.objects.filter(order_id=order_details)
    total_item = 0
    for one in all_orders_details:
        total_item = total_item + one.quantity
    all_food_section = food_section.objects.all().filter(is_active=True,outlet_id=outlet_objects)
    food_objects = food_section.objects.all().filter(outlet_id=outlet_objects).first()
    data ={'order_details':order_details,'all_food_section':all_food_section,'food_objects':food_objects,'all_orders_details':all_orders_details,'total_item':total_item,
            'outlet_objects':outlet_objects,'location':location}
    return render(request,'orders/order_details.html',data)



@login_required(login_url = '/accounts/user_login')
def existing_order_update(request,pk,pk1):
    outlet_objects = outlet.objects.get(pk=pk)
    order_obj = order.objects.get(pk=pk1)
    all_orders_details = customer_order_detail.objects.filter(order_id=order_obj)
    total_amount = 0
    if request.method == "POST":
        for one in all_orders_details:
            dish = dishes.objects.get(pk=request.POST['dish'+ str(one.pk)])
            quantity = request.POST['quantity' + str(one.pk)]

            # try:
            extra_items1 = request.POST.getlist('extra_item1' + str(one.pk))
            for one_item in extra_items1:
                if one_item != "0":
                    extra_item1_cost = one.dish_id.extra_item_cost_1
                    extra_item1 = True
                else:
                    extra_item1_cost = 0
                    extra_item1 = False

                one.extra_item1 = extra_item1
                one.save()
                print('Extra1 : ' + str(extra_items1))

            extra_items2 = request.POST.getlist('extra_item2' + str(one.pk))
            for one_item in extra_items2:
                if one_item != "0":
                    extra_item2_cost = one.dish_id.extra_item_cost_2
                    extra_item2 = True
                else:
                    extra_item2_cost = 0
                    extra_item2 = False

                one.extra_item2 = extra_item2
                one.save()
                
                print('Extra2 : ' + str(extra_items2))

            amount = (int(one.dish_id.amount) * int(quantity)) + extra_item1_cost + extra_item2_cost

            one.dish_id = dish
            one.quantity = quantity
            one.amount = amount
            one.extra_item1 = extra_item1
            one.extra_item2 = extra_item2
            one.save()

            total_amount = total_amount + one.amount
        order_obj.total_bill = total_amount
        order_obj.save()
        return HttpResponseRedirect(reverse('orders:order_details',kwargs={'pk':outlet_objects.pk,'pk1':order_obj.pk}))


@login_required(login_url = '/accounts/user_login')
def add_new_items_existing_order(request,pk,pk1):
    outlet_objects = outlet.objects.get(pk=pk)
    order_obj = order.objects.get(pk=pk1)
    all_dishes =  dishes.objects.filter(is_active=True).all()
    if request.method == "POST":
        selected_dish = []
        not_selected = []
        for one_dish in all_dishes:
            try:
                dish = dishes.objects.get(pk=request.POST['dish'+ str(one_dish.pk)])
            except MultiValueDictKeyError:
                dish = "0"

            quantity = request.POST['quantity' + str(one_dish.pk)]

            try:
                extra_item1 = request.POST['extra1' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item1 = "0"

            try:
                extra_item2 = request.POST['extra2' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item2 = "0"

            if dish != "0":
                selected_dish.append([dish,quantity,extra_item1,extra_item2])
            else:
                not_selected.append([dish,quantity,extra_item1,extra_item2])

        total_amount = order_obj.total_bill
        for item in selected_dish:
            if item[2] == "1":
                extra_item1_cost = item[0].extra_item_cost_1
            else:
                extra_item1_cost = 0

            if item[3] == "1":
                extra_item2_cost = item[0].extra_item_cost_2
            else:
                extra_item2_cost = 0

            total_amount = int(total_amount) + ((int(item[0].amount) * int(item[1])) + int(extra_item1_cost) + int(extra_item2_cost))

        order_obj.total_bill = total_amount
        order_obj.save()
        for one_selected in selected_dish:
            if one_selected[2] == "1":
                extra_item_1 = True
                cost_extra1 = one_selected[0].extra_item_cost_1
            else:
                extra_item_1 = False
                cost_extra1 = 0

            if one_selected[3] == "1":
                extra_item_2 = True
                cost_extra2 = one_selected[0].extra_item_cost_2
            else:
                extra_item_2 = False
                cost_extra2 = 0
            one_amount = int(one_selected[1]) * int(one_selected[0].amount) + int(cost_extra1) + int(cost_extra2)
            customer_order_detail.objects.create(order_id=order_obj,
                                                dish_id=one_selected[0],
                                                quantity=one_selected[1],
                                                amount=one_amount,
                                                extra_item_1=extra_item_1,
                                                extra_item_2=extra_item_2)
    return HttpResponseRedirect(reverse('orders:order_details',kwargs={'pk':outlet_objects.pk,'pk1':order_obj.pk}))


@login_required(login_url = '/accounts/user_login')
def delete_one_item_from_order(request,pk,pk1):
    outlet_objects = outlet.objects.get(pk=pk)
    one_menu_item = customer_order_detail.objects.get(pk=pk1)
    order_obj = order.objects.get(pk=one_menu_item.order_id.pk)
    order_total = order_obj.total_bill
    order_minus = order_total - one_menu_item.amount
    order_obj.total_bill = order_minus
    order_obj.save()
    one_menu_item.delete()
    return HttpResponseRedirect(reverse('orders:order_details',kwargs={'pk':outlet_objects.pk,'pk':order_obj.pk}))


@login_required(login_url = '/accounts/user_login')
def add_new_order_submit(request,pk):
    outlet_objects = outlet.objects.get(pk=pk)
    all_dishes =  dishes.objects.filter(is_active=True,food_section_id__outlet_id=outlet_objects).all()
    if request.method == "POST":
        selected_dish = []
        not_selected = []
        for one_dish in all_dishes:
            try:
                dish = dishes.objects.get(pk=request.POST['dish'+ str(one_dish.pk)])
            except MultiValueDictKeyError:
                dish = "0"

            quantity = request.POST['quantity' + str(one_dish.pk)]
            if quantity != "0":
                quantity = quantity
            else:
                quantity = "0"

            try:
                extra_item1 = request.POST['extra_item1' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item1 = "0"

            try:
                extra_item2 = request.POST['extra_item2' + str(one_dish.pk)]
            except MultiValueDictKeyError:
                extra_item2 = "0"

            if dish != "0":
                selected_dish.append([dish,quantity,extra_item1,extra_item2])
            else:
                not_selected.append([dish,quantity,extra_item1,extra_item2])

        user_name = request.POST['full_name']
        user_mobile = request.POST['mobile_no']
        user_address = request.POST['address']
        landmark = request.POST['landmark']
        payment = request.POST['payment']
        if payment == "1":
            pay = 1
        else:
            pay = 2
        if custom_user.objects.filter(username =user_mobile).exists():
            customuser_obj = custom_user.objects.get(username =user_mobile)
            customer_obj = customer.objects.get(custom_user_id=customuser_obj)
            number = random.randint(1000, 9999)
            customuser_obj.otp = number
            customuser_obj.save()
        else:
            number = random.randint(1000, 9999)
            customuser_obj = custom_user.objects.create(username=user_mobile,
                                                        mobile_no=user_mobile,
                                                        password=make_password(user_mobile),
                                                        user_role=3,
                                                        otp=number)
            customer_obj = customer.objects.create(custom_user_id=customuser_obj,
                                                # outlet_id = outlet_objects,
                                                full_name=user_name,
                                                address=user_address)
        total_amount = 0
        for item in selected_dish:
            if item[2] == "1":
                extra_item1_cost = item[0].extra_item_cost_1
            else:
                extra_item1_cost = 0

            if item[3] == "1":
                extra_item2_cost = item[0].extra_item_cost_2
            else:
                extra_item2_cost = 0

            total_amount = total_amount + (int(item[0].amount) * int(item[1])) + int(extra_item1_cost) + int(extra_item2_cost)

        todays_date = date.today()
        order_id = str(customuser_obj.username[:4]) + "/" + str(todays_date.day) + "" + str(todays_date.month) + "/" + str(todays_date.year)
        order_obj = order.objects.create(order_id=order_id,
                                        outlet_id = outlet_objects,
                                        customer_id=customer_obj,
                                        payment_type=pay,
                                        order_delivery_address=user_address,
                                        landmark=landmark,
                                        total_bill=total_amount,
                                        order_status=1)
        for one_selected in selected_dish:
            if one_selected[2] == "1":
                extra_item_1 = True
                cost_extra1 = one_selected[0].extra_item_cost_1
            else:
                extra_item_1 = False
                cost_extra1 = 0

            if one_selected[3] == "1":
                extra_item_2 = True
                cost_extra2 = one_selected[0].extra_item_cost_2
            else:
                extra_item_2 = False
                cost_extra2 = 0
            one_amount = int(one_selected[1]) * int(one_selected[0].amount) + int(cost_extra1) + int(cost_extra2)
            customer_order_detail.objects.create(order_id=order_obj,
                                                dish_id=one_selected[0],
                                                quantity=one_selected[1],
                                                amount=one_amount,
                                                extra_item_1=extra_item_1,
                                                extra_item_2=extra_item_2)
    return HttpResponseRedirect(reverse('orders:new_order',kwargs={'pk':outlet_objects.pk}))