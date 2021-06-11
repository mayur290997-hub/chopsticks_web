from django.urls import include, path
from dishes.views import *

app_name = 'dishes'

urlpatterns = [
path('all_dishes/<int:pk>/<int:pk1>',all_dishes,name='all_dishes'),

path('menu/<int:pk>',menu,name='menu'),

path('add_dishes/<int:pk>/<int:pk1>',add_dishes,name='add_dishes'),

path('update_dish/<int:pk>/<int:pk1>/<int:pk2>',update_dish,name='update_dish'),

path('delete_dish/<int:pk>/<int:pk1>/<int:pk2>',delete_dish,name='delete_dish'),

]