from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from food_section.models import food_section
from dishes.models import dishes
from outlet.models import outlet
# Create your views here.

@login_required(login_url = '/accounts/user_login')
def food_section_master(request,pk):
    user = request.user
    location = outlet.objects.all().filter(is_active=True)
    outlet_objects = outlet.objects.get(pk=pk)
    # location = outlet.objects.all()
    all_section = food_section.objects.all().filter(outlet_id=outlet_objects)
    outlet_object = outlet.objects.all().filter(is_active=True)
    item_count = {}
    for one in all_section:
        if dishes.objects.filter(food_section_id=one).exists():
            item_count[one.pk] = dishes.objects.filter(food_section_id=one).count()
        else:
            item_count[one.pk] = 0
    food_objects = all_section.first()
    data = {'all_section':all_section,'food_objects':food_objects,'item_count':item_count,'outlet_objects':outlet_objects,'location':location}
    return render(request, 'food_section/add_section.html',data)


@login_required(login_url = '/accounts/user_login')
def food_add(request,pk):
    user= request.user
    outlet_objects = outlet.objects.get(pk=pk)
    all_section=food_section.objects.all()
    food_objects = all_section.first()
    outlet_object = outlet.objects.all().filter(is_active=True)
    if request.method == "POST":
        section_name = request.POST['section_name']
        outlet_id = outlet.objects.get(pk=request.POST['outlet_id'])

        if food_section.objects.filter(section_name=section_name,outlet_id=outlet_objects).exists():
            error_msg='Food Section Name Already Exist!'
            data={'error_msg':error_msg,'food_objects':food_objects,'all_section':all_section,'outlet_object':outlet_object}
            return render(request,'food_section/add_section.html',data)
        else :
            food_section.objects.create(section_name=section_name,
                                        outlet_id=outlet_id)
            return HttpResponseRedirect(reverse('food_section:food_section_master',kwargs={'pk':outlet_objects.pk}))
    else:
        data={'food_objects':food_objects,'all_section':all_section,'outlet_object':outlet_object}
        return render (request,'food_section/add_section.html',data)


@login_required(login_url = '/accounts/user_login')
def food__section_update(request,pk,pk1):
    user= request.user
    outlet_objects = outlet.objects.get(pk=pk)
    food_obj = food_section.objects.get(pk=pk1)
    location = outlet.objects.all().filter(is_active=True)
    all_section=food_section.objects.all()
    food_objects = all_section.first()
    if request.method == "POST":
        section_name = request.POST['section_name']
        is_active = request.POST['is_active']
        if food_section.objects.filter(section_name=section_name,outlet_id=outlet_objects).exclude(section_name=food_obj.section_name).exists():
            error_msg='Food Section Name Already Exist!'
            data={'error_msg':error_msg,'food_objects':food_objects,'all_section':all_section,'location':location,'outlet_objects':outlet_objects}
            return render(request,'food_section/add_section.html',data)
        else:
            food_obj.section_name = section_name
            food_obj.is_active = is_active
            food_obj.save()
            return HttpResponseRedirect(reverse('food_section:food_section_master',kwargs={'pk':outlet_objects.pk}))
