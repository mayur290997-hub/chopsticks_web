from django.urls import include, path
from customer.views import *

app_name = 'customer'

urlpatterns = [
path('customer_master',customer_master,name='customer_master'),

# path('add_new_customer',add_new_customer,name='add_new_customer'),

path('update_customer/<int:pk>/<int:pk1>',update_customer,name='update_customer'),

path('customer_detail/<int:pk>/<int:pk1>',customer_detail,name='customer_detail'),

path('delete_order/<int:pk>/<int:pk1>',delete_order,name='delete_order'),

]