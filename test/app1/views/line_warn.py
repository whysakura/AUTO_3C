from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
import json, time, random
import datetime
# Create your views here.
from app1.my_time import my_time

# 产线站点报警
def line_warn(request):
    line_time = time.time()  # 时间
    data = json.loads(request.body.decode('utf-8'))
    line_id = data['line_id'].upper()  # 车间号
    line_station = data['line_station']  # 线体
    type = data['type']  # 报警号
    print(line_id, line_station,type)
    if type == '1':
        if Line_warn.objects.filter(line_id_id=line_id, line_station__station_id=line_station, line_status='1'):
            print('已经存在')
            return HttpResponse('existed')
        try:
            line = Line_warn()
            l=Line.objects.get(line_id=line_id)
            s=Station.objects.get(station_id=line_station)
            line.line_id = l
            line.line_station = s
            line.start_time = line_time
            line.line_status = type
            line.save()
        except:
            return HttpResoponse('false')
        print('1ok')
        return HttpResponse('ok')
    elif type == '2':
        a = Line_warn.objects.filter(line_id_id=line_id, line_station__station_id=line_station, line_status='1')
        if a:
            total_time=my_time(a[0].start_time,line_time)
            print(total_time)
            a.update(line_status=type, end_time=line_time,total_time=total_time)
            print('2ok')
            return HttpResponse('ok')
        else:
            print('2false')
            return HttpResponse('false')
    elif type == '3':
        a = Line_warn.objects.filter(line_id_id=line_id, line_station__station_id=line_station).order_by('-id')[0]
        if a.line_status == '2':
            print('3ok')
            return HttpResponse(line_id + line_station)
        print('3false')
        return HttpResponse('false')
    else:
        return HttpResponse('error number')