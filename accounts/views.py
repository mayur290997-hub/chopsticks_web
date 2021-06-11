from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from  accounts.models import custom_user
from customer.models import customer
from outlet.models import outlet
from food_section.models import food_section
import random

# Create your views here.
def home(request):
    outlet_objects = outlet.objects.all().filter(is_active=True)
    food_section1 = food_section.objects.filter(outlet_id=outlet_objects)
    data ={'outlet_objects':outlet_objects,'food_section1':food_section1}
    return render(request, 'accounts/home.html',data)


def user_login(request):
    """Logs in a user if the credentials are valid and the user is active,
    else redirects to the same page and displays an error message."""
    # outlet_objects = outlet.objects.all()
    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('customer:customer_master'))
        else:
            return render(request, 'accounts/login.html',{'error_message': 'Username or Password Incorrect!'})
    else:
        return render(request, 'accounts/login.html')



@login_required(login_url = '/accounts/user_login')
def user_logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('accounts:user_login'))


def web_login(request):
    if request.method == "POST":
        mobile_no= request.POST['mobile_no']
        if custom_user.objects.filter(mobile_no=mobile_no).exists():
            user = custom_user.objects.get(mobile_no=mobile_no)
            # if custom_user.objects.filter(user_role=3) :
            number = random.randint(1000, 9999)
            user.otp = number
            user.save()
            return HttpResponseRedirect(reverse('accounts:user_otp',kwargs= {'pk':user.pk}))
        else:
            number = random.randint(1000, 9999)
            user_object = custom_user.objects.create(username=mobile_no,
                                                    password = make_password(mobile_no),
                                                    mobile_no = mobile_no,
                                                    otp=number,
                                                    user_role = 3)
            customer_objects = customer.objects.create(custom_user_id=user_object)
            return HttpResponseRedirect(reverse('accounts:user_otp',kwargs= {'pk':user_object.pk}))
    else :
        return render (request , 'accounts/web_login.html')

def user_otp(request,pk):
    user = custom_user.objects.get(pk=pk)
    if request.method == "POST":
        otp_num = request.POST['otp1'] + request.POST['otp2'] + request.POST['otp3'] + request.POST['otp4']
        if user.otp == int(otp_num):
            login(request, user)
            return HttpResponseRedirect(reverse('orders:cust_order_details'))
        else:
            data={'user':user,'erroe_msg':"OTP Does not match!!!"}
            return render(request,'accounts/otp.html',data)
    else:
        data={'user':user}
        return render(request,'accounts/otp.html',data)
    # data = {'user':user}
    return render (request , 'accounts/otp.html')


@login_required(login_url = '/accounts/web_login')
def web_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:web_login'))