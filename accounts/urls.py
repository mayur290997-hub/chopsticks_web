from django.urls import include, path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
path('user_login',user_login,name='user_login'),

path('logout',user_logout,name='logout'),

path('web_login',web_login,name='web_login'),

path('user_otp/<int:pk>',user_otp,name='user_otp'),

path('home',home,name='home'),

path('web_logout',web_logout,name='web_logout'),

]