from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from dishes.models import dishes
from food_section.models import food_section
from extra_item.models import extra_item
from outlet.models import outlet
# Create your views here.


def menu(request,pk):
    outlet_objects = outlet.objects.get(pk=pk)
    # food_objects = food_section.objects.filter()
    food_section1 = food_section.objects.all().filter(is_active=True,outlet_id=outlet_objects)
    location = outlet.objects.all().filter(is_active=True)
    all_dish=dishes.objects.all().filter(food_section_id=food_section1,is_active=True,food_section_id__outlet_id=outlet_objects)
    data={'all_dish':all_dish,'food_section1':food_section1,'location':location,'outlet_objects':outlet_objects}
    return render (request, 'dishes/menu.html',data)

@login_required(login_url = '/accounts/user_login')
def all_dishes(request,pk,pk1):
    user = request.user
    outlet_objects = outlet.objects.get(pk=pk)
    food_objects = food_section.objects.get(pk=pk1)
    location = outlet.objects.all().filter(is_active=True)
    food_section1 = food_section.objects.all().filter(is_active=True,outlet_id=outlet_objects)
    all_dish=dishes.objects.all().filter(food_section_id=food_objects,is_active=True,food_section_id__outlet_id=outlet_objects)
    data={'all_dish':all_dish,'food_objects':food_objects,'food_section1':food_section1,'location':location,'outlet_objects':outlet_objects}
    return render(request,'dishes/all_dishes.html',data)


@login_required(login_url = '/accounts/user_login')
def add_dishes(request,pk,pk1):
    user = request.user
    location = outlet.objects.all().filter(is_active=True)
    outlet_objects = outlet.objects.get(pk=pk)
    food_objects = food_section.objects.get(pk=pk1)
    if request.method == "POST":
        dish_type = request.POST['dish_type']
        dish_name = request.POST['dish_name']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        extra_item_1 = request.POST['extra_item_1']
        extra_item_2 = request.POST['extra_item_2']
        extra_item_cost_1 = request.POST['extra_item_cost_1']
        extra_item_cost_2 = request.POST['extra_item_cost_2']
        if extra_item_cost_1 == "":
            extra_item_cost_1 = 0
        else:
            extra_item_cost_1 = extra_item_cost_1

        if extra_item_cost_2 == "":
            extra_item_cost_2 = 0
        else:
            extra_item_cost_2 = extra_item_cost_2

        if dishes.objects.filter(dish_name = dish_name,food_section_id__outlet_id=outlet_objects).exists():
            error_msg='Dish Name already exist !'
            extra_item_objects = extra_item.objects.all()
            food_section1 = food_section.objects.all()
            all_dish=dishes.objects.all().filter(food_section_id=food_objects)
            data={'error_msg':error_msg,'all_dish':all_dish,'food_objects':food_objects,'food_section1':food_section1,'extra_item_objects':extra_item_objects}
            return render(request,'dishes/all_dishes.html',data)
        else:
            dish = dishes.objects.create(food_section_id=food_objects,
                                        dish_type=dish_type,
                                        dish_name=dish_name,
                                        quantity=quantity,
                                        amount=amount,
                                        extra_item_1=extra_item_1,
                                        extra_item_2=extra_item_2,
                                        extra_item_cost_1=extra_item_cost_1,
                                        extra_item_cost_2=extra_item_cost_2)
            return HttpResponseRedirect(reverse('dishes:all_dishes',kwargs={'pk':outlet_objects.pk,'pk1':food_objects.pk}))


@login_required(login_url = '/accounts/user_login')
def update_dish(request,pk,pk1,pk2):
    user = request.user
    outlet_objects = outlet.objects.get(pk=pk)
    food_objects = food_section.objects.get(pk=pk1)
    location = outlet.objects.all().filter(is_active=True)
    all_dish=dishes.objects.get(pk=pk2)
    if request.method == "POST":
        dish_type = request.POST['dish_type']
        dish_name = request.POST['dish_name']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        extra_item_1 = request.POST['extra_item_1']
        extra_item_2 = request.POST['extra_item_2']
        extra_item_cost_1 = request.POST['extra_item_cost_1']
        extra_item_cost_2 = request.POST['extra_item_cost_2']
        all_dish.dish_type=dish_type
        all_dish.dish_name=dish_name
        all_dish.quantity=quantity
        all_dish.amount=amount
        all_dish.extra_item_1=extra_item_1
        all_dish.extra_item_2=extra_item_2
        all_dish.extra_item_cost_1=extra_item_cost_1
        all_dish.extra_item_cost_2=extra_item_cost_2
        all_dish.save()
        return HttpResponseRedirect(reverse('dishes:all_dishes',kwargs={'pk':outlet_objects.pk,'pk1':food_objects.pk}))


@login_required(login_url = '/accounts/user_login')
def delete_dish(request,pk,pk1,pk2):
    user = request.user
    outlet_objects = outlet.objects.get(pk=pk)
    food_objects = food_section.objects.get(pk=pk1)
    all_dish=dishes.objects.get(pk=pk2)
    if all_dish.is_active == True:
        all_dish.is_active = False
        all_dish.save()
    else:
        all_dish.is_active = True
        all_dish.save()
    return HttpResponseRedirect(reverse('dishes:all_dishes',kwargs={'pk':outlet_objects.pk,'pk1':food_objects.pk}))
