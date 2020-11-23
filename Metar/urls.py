from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('metar/ping', views.sample_server_check, name='check_sever_stats'),
    path('metar/info', views.view_data, name='data')
]