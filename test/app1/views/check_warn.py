from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
import json, time, random
from itertools import chain
from django.core import serializers
from Agv import AgvCar
import sys, os
import threading
import datetime

from app1.my_time import my_time
from app1.my_time import timeTodatetime
# Create your views here.

#终端检查报警
def check_warn(request):
    data = json.loads(request.body.decode('utf-8'))
    line_id = data['line_id'].upper()  # 车间号
    try:
        a = Line_warn.objects.filter(line_id_id=line_id, line_status='1').order_by('id').values('line_station__station_id','line_status','line_id_id','start_time')
        # print(json.dumps(list(a)))
        for i in range(0, len(a)):
            a[i]['start_time'] = timeTodatetime(a[i]['start_time'])
            # a[i]['end_time'] = timeTodatetime(a[i]['end_time'])
        a = json.dumps(list(a))
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('null')
