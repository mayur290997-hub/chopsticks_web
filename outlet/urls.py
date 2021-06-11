from django.urls import include, path
from outlet.views import *

app_name = 'outlet'

urlpatterns = [

path('outlet_master',outlet_master,name='outlet_master'),

path('add_outlet',add_outlet,name='add_outlet'),

path('delete_outlet/<int:pk>',delete_outlet,name='delete_outlet'),

]