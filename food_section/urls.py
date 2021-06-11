from django.urls import include, path
from food_section.views import *

app_name = 'food_section'

urlpatterns = [

path('food_add/<int:pk>',food_add,name='food_add'),

path('food_section_master/<int:pk>',food_section_master,name='food_section_master'),

path('food__section_update/<int:pk>/<int:pk1>',food__section_update,name='food__section_update'),

]