
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



# 创建订单号
def create_order(line_id):
    a = time.strftime('%Y%m%d%H%M%S')
    a = 'CIG'+line_id+'_' + a
    items = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'q', 'w', 'e', 'r',
             't', 'y', 'u', 'i', 'p', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
    random.shuffle(items)
    num = a + str('').join(items)[0:5]
    if Order.objects.filter(order_sn=num):
        create_order()
    return num


def material_request(request):
    data = json.loads(request.body.decode('utf-8'))
    line_id = data['0']['line_id'].upper()
    wtype = data['0']['type']
    station=data['0']['station']
    or_num = create_order(line_id)
    if wtype == '1' and len(data) == 2:
        print('送完成品的只有一个点')
        return HttpResponse('error')
    if Order.objects.filter(line_id_id=line_id,station_id__station_id=station, order_status='未完成'):
        print('未完成')
        return HttpResponse('existed')

    for a, b in data.items():
        print(b['count'],line_id, b['gid'])
        gid = b['gid']
        count = b['count']
        if line_id == '' or gid == '' or count == '' or station=='':
            print('少参数')
            return HttpResponse('')
        # if Order.objects.all().count()>1000000:
        if not Order.objects.filter(order_sn=or_num):
            date = time.time()
            li_num = Line.objects.all().get(line_id=line_id)
            st=Station.objects.get(station_id=station,station_mark__line_id_id=line_id)
            print(li_num,st)
            o = Order()
            o.line_id = li_num
            o.station_id=st
            o.order_sn = or_num
            o.order_time = date
            o.work_type = wtype

            o.save()
            print('总订单数目' + str(Order.objects.all().count()))

        ordd = Order.objects.get(order_sn=or_num)
        goid = Goods.objects.get(goods_id=gid,goods_line_id=line_id)
        o_de = Order_property()
        o_de.order_sn = ordd
        o_de.goods_id = goid
        o_de.order_count = count
        o_de.save()
    return HttpResponse(or_num + '<br/>' + line_id + '<br/>'+ station + '<br/>' + str(date))
