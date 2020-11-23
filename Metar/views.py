from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import os, redis, traceback
from . import helper
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django_redis import get_redis_connection
from django.views.decorators.cache import cache_page
from metar import Metar

path = settings.BASE_DIR
try:
    redis_conn = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
    server_start = True
except:
    traceback.print_exc()
    server_start = False

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def index(request):
    
    server_status = ''

    if server_start:
        server_status = "Server Started!"

    else:
        server_status = "Server Failed to Start!"

    context = {

        "server_status" : server_status,
    }
    return render(request, 'metar/metar.html', context)



@cache_page(CACHE_TTL) 
def view_data(request):
   
    err_msg = ''
    message = ''
    message_class = ''
    server_status = ''

    if server_start:
        server_status = "Server Started!"

        code = request.GET.get('scode')
        redis_conn.get(code)

        meta_info = helper.get_station_info(code)

        if meta_info['data'] is not None:
            obj = Metar.Metar(meta_info['data'], strict=False)
            
            observation_time = helper.get_time(obj.time) 
            station_id = obj.station_id
            observation_temp = helper.get_temp(obj.temp)
            speed = helper.get_speed(str(obj.wind_speed))
            wind_direction = str(obj.wind_dir)

            context = {

                "message" : meta_info['message'],
                "message_class" : meta_info['message_class'],
                "fetch_status" : True,
                "observation_time" : observation_time,
                "station_id" : station_id,
                "observation_temp" : observation_temp,
                "speed" : speed,
                "wind_direction" : wind_direction,
                "server_status" : server_status,
                
            }

            redis_conn.set(station_id, station_id)

            return render(request, "metar/metar.html", context)

        else:
            context = {
                "message" : meta_info['message'],
                "fetch_status" : False,
                "message_class" : meta_info['message_class'],
                "server_status" : server_status,
            }

            redis_conn.set(code, code)
            return render(request, "metar/metar.html", context)

    else:

        server_status = "Server Failed to Start!"
        raise Exception(server_status)

    return HttpResponse("Welcome to Metar Data World!!")    


def sample_server_check(request):


    if server_start:
        context = {
            "data" : "pong"
        }
        return JsonResponse(context, safe=False)
    else:
        context = {
            "data" : "Server Could not start!"
        }
        return JsonResponse(context, safe=False)
    
    return HttpResponse("Server Check!")