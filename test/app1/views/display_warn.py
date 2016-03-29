from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *
import json, time, random
import sys, os
from app1.my_time import my_time
from app1.my_time import timeTodatetime
# Create your views here.


#显示历史告警服务请求记录
def display_warn(request):
    # data = json.loads(request.body.decode('utf-8'))
    # line_id = data['line_id'].upper()  # 车间号
    line_id=request.GET.get('line_id','3C')
    try:
        a = Line_warn.objects.filter(line_id_id=line_id, line_status='2').order_by('id').values('line_station__station_id','end_time','line_status','total_time','line_id_id','start_time')
        # start_date = datetime.datetime(2016,3,22,15,5)
        # now_date=datetime.datetime.now()
        # b=Line_warn.objects.filter(line_id=line_id, line_status='2',start_time__range=(start_date,now_date)).order_by('id').values()
        # print(b)
        # print(json.dumps(list(a)))
        # a = json.dumps(list(a))
        for i in range(0, len(a)):
            a[i]['start_time'] = timeTodatetime(a[i]['start_time'])
            a[i]['end_time'] = timeTodatetime(a[i]['end_time'])
        print(a)
        return render(request, 'display_warn.html', locals())
    except:
        return HttpResponse('error')
