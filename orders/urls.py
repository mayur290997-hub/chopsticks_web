from django.urls import include, path
from orders.views import *

app_name = 'orders'

urlpatterns = [

path('select_order_item/<int:pk>',select_order_item,name='select_order_item'),

path('order_placed/<int:pk>',order_placed,name='order_placed'),

path('success_order/<int:pk>',success_order,name='success_order'),


path('order_master/<int:pk>',order_master,name='order_master'),

path('cust_order_details',cust_order_details,name='cust_order_details'),

path('order_cancle/<int:pk>',order_cancle,name='order_cancle'),

path('today_order/<int:pk>',today_order,name='today_order'),

path('update_status/<int:pk>/<int:pk1>',update_status,name='update_status'),

path('new_order/<int:pk>',new_order,name='new_order'),

path('order_details/<int:pk>/<int:pk1>',order_details,name='order_details'),

path('get_customer_detail',get_customer_detail,name='get_customer_detail'),

path('existing_order_update/<int:pk>/<int:pk1>',existing_order_update,name='existing_order_update'),

path('add_new_items_existing_order/<int:pk>/<int:pk1>',add_new_items_existing_order,name='add_new_items_existing_order'),

path('add_new_order_submit/<int:pk>',add_new_order_submit,name='add_new_order_submit'),

path('delete_one_item_from_order/<int:pk>/<int:pk1>',delete_one_item_from_order,name='delete_one_item_from_order'),
]