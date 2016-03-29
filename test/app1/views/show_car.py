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



# 显示小车路线
def show_car(request):
    line_id='3C'
    alldata = []
    l = {
        'None':'None',
        '0': '空置',
        '1': '取料',
        '2': '装料',
        '3': '送料',
        '4': '完成',
        '5': '无任务返回原地',
    }
    for a in range(1, 6):
        # 返回所需数据
        lists = []
        lists.append(line_id)
        lists.append(a)
        car = Car.objects.get(car_number=str(a))
        data = Car.objects.select_related().all().values(
            'car_status',
            'car_mark__mark_id',
            'distination',
        ).filter(car_number=str(a),line_id_id=line_id,car_mark__line_id_id=line_id)
        data[0]['car_status']=l[data[0]['car_status']]
        lists.append(data[0]['car_status'])
        if data[0]['car_mark__mark_id']:
            lists.append(data[0]['car_mark__mark_id'] + '号mark点')
        else:
            lists.append(data[0]['car_mark__mark_id'])
        d = data[0]['distination']
        print(d)
        if d == '':
            lists.append(data[0]['distination'])
        else:
            mk=Mark.objects.get(mark_id=d,line_id_id=line_id)
            st = Station.objects.get(station_mark=mk).station_id
            print(st)
            if st == '0':
                st = '取料点'
            else:
                st = st + '号站点'
            lists.append(st)
        alldata.append(lists)
    print(alldata)
    if Mark.objects.filter(mark_status='1'):
        print(Mark.objects.filter(mark_status='1'))
    # 转换为jsonstr
    data = json.dumps(list(alldata), ensure_ascii=False)

    # json转为list
    # data=json.loads(data)
    # print(type(data))
    return HttpResponse(data)

