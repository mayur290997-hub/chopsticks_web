from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta,datetime
from django.http import JsonResponse

from outlet.models import outlet
from food_section.models import food_section
# Create your views here.

def outlet_master(request):
    outlet_objects = outlet.objects.all()
    food_objects = food_section.objects.all()
    data = {'outlet_objects':outlet_objects,'food_objects':food_objects}
    return render (request,'outlet/outlet_master.html',data)


def add_outlet(request):
    user = request.user
    all_outlet = outlet.objects.all()
    outlet_objects = all_outlet.first()
    if request.method == "POST":
        outlet_name = request.POST['outlet_name']
        outlet_location = request.POST['outlet_location']
        outlet_image = request.POST['outlet_image']

        if outlet.objects.filter(outlet_name=outlet_name).exists():
            error_msg='Outlet Name Name Already Exist!'
            data={'error_msg':error_msg,'outlet_objects':outlet_objects,'all_outlet':all_outlet}
            return render(request,'outlet/outlet_master.html',data)
        else:
            outlet.objects.create(outlet_name=outlet_name,
                                    outlet_location=outlet_location,
                                    outlet_image=outlet_image
                                    )
            return HttpResponseRedirect(reverse('outlet:outlet_master'))
    else:
        data={'all_outlet':all_outlet,'outlet_objects':outlet_objects}
        return render (request,'outlet/outlet_master.html',data)

def delete_outlet(request,pk):
    user= request.user
    outlet_obj = outlet.objects.get(pk=pk)
    all_outlet=outlet.objects.all()
    outlet_objects = all_outlet.first()
    if request.method == "POST":
        outlet_name = request.POST['outlet_name']
        outlet_location = request.POST['outlet_location']
        outlet_image = request.POST['outlet_image']
        is_active = request.POST['is_active']
        if outlet.objects.filter(outlet_name=outlet_name).exclude(outlet_name=outlet_obj.outlet_name).exists():
            error_msg='outlet Name Already Exist!'
            data={'error_msg':error_msg,'outlet_objects':outlet_objects,'all_outlet':all_outlet}
            return render(request,'outlet/outlet_master.html',data)
        else:
            outlet_obj.outlet_name = outlet_name
            outlet_obj.outlet_location = outlet_location
            outlet_obj.outlet_image = outlet_image
            outlet_obj.is_active = is_active
            outlet_obj.save()
            return HttpResponseRedirect(reverse('outlet:outlet_master'))