from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
import time, datetime
from app1.my_time import my_time
from app1.my_time import timeTodatetime


# Create your views here.

# 显示未完成订单
def show_order(request):
    data = Order_property.objects.select_related().all().values(
        'order_sn__line_id_id',
        'order_sn__station_id__station_id',
        'order_sn__order_sn',
        'order_sn__order_status',
        'order_sn__station_id__station_mark__mark_id',
        'order_sn__order_time',
        'order_sn__car_number__car_number',
        'order_sn__car_number__car_status',
    ).filter(order_sn__order_status='未完成',
             order_sn__line_id_id='3C',
             )
    print(data)
    data = list(data)
    l = {
        'None':'None',
        '0': '空置',
        '1': '取料',
        '2': '装料',
        '3': '送料',
        '4': '完成',
        '5': '无任务返回原地',
    }
    for i in range(0, len(data)):
        if data[i]['order_sn__car_number__car_status']:
            data[i]['order_sn__car_number__car_status']=l[data[i]['order_sn__car_number__car_status']]
        data[i]['order_sn__order_time'] = timeTodatetime(data[i]['order_sn__order_time'])
    return render(request, 'show.html', locals())
