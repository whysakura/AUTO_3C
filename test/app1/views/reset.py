from django.shortcuts import render
from django.http import HttpResponse
from app1.models import *


# 恢复出厂设置
def reset(request):
    #Line初始化
    try:
        line_id=['3C','3B','3A']
        l=Line()
        for i in line_id:
            l.line_id=i
            l.save()
    except:
        print('Line reset error')
        return HttpResponse('Line reset error')

    # Mark的初始化
    try:
        next_mark={
            '3C':{99: 35, 34: 35,
                  37: 38, 92: 38,
                  40: 41, 85: 41,
                  43: 44, 78: 44,
                  46: 47, 71: 47,
                  49: 50, 64: 50},
        }
        for i in range(0, 100):
            mm = Mark()
            try:
                mm=Mark.objects.get(mark_id=str(i),line_id_id='3C')
            except:
                pass
            l=Line.objects.get(line_id='3C')
            mm.line_id=l
            mm.mark_id = str(i)
            mm.mark_status = '0'
            print(i)
            if i in next_mark['3C']:
                print(i, next_mark['3C'][i])
                mm.next_mark = str(next_mark['3C'][i])
            mm.save()
    except:
        print('Mark reset error')
        return HttpResponse('Mark reset error')


    #Station初始化
    station = {
        '3C':[1,
             30, 29, 28, 27,
             98, 97, 96, 95,
             98, 97, 96, 95,
             91, 90, 89, 88,
             91, 90, 89, 88,
             84, 83, 82, 81,
             84, 83, 82, 81,
             77, 76, 75, 74,
             77, 76, 75, 74,
             70, 69, 68, 67,
             70, 69, 68, 67,
             63, 62, 61, 60,
             ]
    }
    c3 = 0

    try:
        for i in station['3C']:
            sta=Station()
            try:
                sta=Station.objects.get(station_id=c3,station_mark__line_id_id='3C')
            except:
                pass
            mark=Mark.objects.get(mark_id=i,line_id__line_id='3C')
            sta.station_mark=mark
            sta.station_id=c3
            print(mark,c3)
            c3 = c3 + 1
            sta.save()
    except:
        print('station reset error')
        return HttpResponse('Station reset error')

    #Goods初始化

    c3=[['3C','1','底壳','纸质','0',0],]
    try:
        for i in c3:
            l=Line.objects.get(line_id=i[0])
            g=Goods()
            g.goods_line=l
            g.goods_id=i[1]
            g.goods_name=i[2]
            g.goods_type=i[3]
            s=Station.objects.get(station_id=i[4])
            g.goods_station=s
            print(i)
            g.goods_counts=i[5]
            g.save()
    except:
        print('goods reset error')
        return HttpResponse('goods reset error')


    # # Car的初始化
    try:
        for i in range(1, 6):
            car = Car()
            try:
                car=Car.objects.get(car_number=str(i),line_id_id='3C')
            except:
                pass
            car.car_number = str(i)
            l=Line.objects.get(line_id='3C')
            car.line_id=l
            car.car_status = '0'
            m=Mark.objects.get(mark_id='0',line_id='3C')
            car.car_mark = m
            car.default_mark = '1'
            car.distination = ''
            car.save()
            print(i)
    except:
        print('Car reset error')
        return HttpResponse('Car reset error')
    return HttpResponse('ok')
