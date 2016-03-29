from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
from app1.my_time import my_time
from app1.my_time import timeTodatetime
# Create your views here.

# 显示完成订单
def end_order(request):
    data = Order_property.objects.select_related().all().values(
        'order_sn__line_id_id',
        'order_sn__order_sn',
        'order_sn__station_id__station_id',
        'order_sn__order_status',
        'order_sn__order_time',
        'order_sn__car_number__car_number',
        'order_sn__finish_time',
        'order_sn__total_time',
    ).filter(order_sn__order_status='完成')
    data = list(data)

    for i in range(0, len(data)):
        data[i]['order_sn__total_time'] = my_time(data[i]['order_sn__finish_time'],data[i]['order_sn__order_time'])
        data[i]['order_sn__order_time'] = timeTodatetime(data[i]['order_sn__order_time'])
        data[i]['order_sn__finish_time'] = timeTodatetime(data[i]['order_sn__finish_time'])
    return render(request, 'end.html', locals())
