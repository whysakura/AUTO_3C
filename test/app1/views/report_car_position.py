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

class Ag:
    c = AgvCar.AgvCar(r'E:\wrd\3C\test\Agv\3c_path\3c_agv_file', r'E:\wrd\3C\test\Agv\3c_path\turn.csv',
                      r'E:\wrd\3C\test\Agv\3c_path\distance.csv')

    def get():
        return Ag.c


# 接受小车状态
def report_car_position(request):
    car_data = json.loads(request.body.decode('utf-8'))
    line_id = car_data['line_id'].upper()
    status = car_data['car_status']
    car_number = car_data['car_number']
    if 'position' in car_data.keys():
        pos = car_data['position']
    print(car_data)
    car = Car.objects.get(car_number=car_number,line_id_id=line_id)#car 的get获取对象
    carr = Car.objects.filter(car_number=car_number,line_id_id=line_id)#car 的filter获取query集

    tm = time.time()
    if int(status) == 0:

        # 判断是不是重复发送
        try:
            order = Order.objects.filter(line_id_id=line_id,order_status="未完成", car_number=car)[0]
            #小车出发时的时候，取消当前点的占用状态
            Mark.objects.filter(mark_id=car.distination,line_id_id=line_id).update(mark_status='0')
        except:

            pass
        else:
            # 返回站点代码
            if carr.filter(car_status='3'):
                # 先判断是哪个工作类型
                if order.work_type == '1':
                    # 物料站点号
                    carr.update(distination='0x03')
                    print('去完成品地点0x03')
                    # 存入小车下一个目的地
                    carr.update(distination='0x03')
                    return HttpResponse('0x03')
                else:
                    # 站点号
                    station_mark = order.station_id.station_mark.mark_id
                    print('站xx点mark->' + station_mark)
                    # 存入小车下一个目的地
                    carr.update(distination=station_mark)
                    return HttpResponse(station_mark)

                    # 如果重复发1，判断工作类型
            # if car.filter(car_status='1'):
            #     # 返回站点
            #     if order.work_type == '1':
            #         line_number = order.line_id  # 线体号
            #         zd = Line.objects.filter(line_id=line_number)[0]
            #         print('先去站点' + zd.line_mark)
            #         # 存入小车下一个目的地
            #         carr.update(distination=zd.line_mark)
            #         return HttpResponse(zd.line_mark)
            #     else:
            #         # 物料站点号
            #         gid = order.order_property_set.filter(order_status='0').values().order_by('goods_id')[0][
            #             'goods_id_id']
            #         sn = Goods.objects.filter(goods_id=gid)[0]
            #         print('物@料' + sn.goods_mark)
            #         # 存入小车下一个目的地
            #         carr.update(distination=sn.goods_mark)
            #         return HttpResponse(sn.goods_mark)

            elif carr.filter(car_status='2'):
                # 两个以上的物料点
                # if order.order_property_set.all().count()>1:
                # 	sta=Car_status.objects.all().get(number='1')
                # 	car.car_status=sta
                # 	car.save()
                # 	orsn=order.order_property_set.all().values().order_by('goods_id')[0]['order_sn_id']
                # 	#查询未完成的物料点
                # 	if Order_property.objects.filter(order_sn=orsn,order_status='0'):
                # 		#物料站点号
                # 		gid=order.order_property_set.filter(order_status='0').values().order_by('goods_id')[0]['goods_id_id']
                # 		sn=Goods.objects.filter(goods_id=gid)[0]
                # 		print('物x料'+sn.goods_mark)
                # 		#存入小车下一个目的地
                # 		carr.update(distination=sn.goods_mark)
                # 		return HttpResponse(sn.goods_mark)
                # 状态改为3

                car.car_status = '3'
                car.save()
                # 先判断是哪个工作类型
                if order.work_type == '1':
                    pass
                else:
                    # 站点号
                    station_mark = order.station_id.station_mark.mark_id
                    print('站点mark->' + station_mark)
                    # 存入小车下一个目的地
                    carr.update(distination=station_mark)
                    return HttpResponse(station_mark)
            else:
                print('状态0错误')
                return HttpResponse()

        # 分配任务
        if Order.objects.filter(line_id_id=line_id,order_status="未完成", car_number=None) and carr.filter(car_mark__mark_id='1'):

            order = Order.objects.filter(line_id_id=line_id,order_status="未完成", car_number=None).order_by('id')[0]
            # if order.work_type == '1':  # 判断先去哪个目的地
            #     line_number = order.line_id  # 线体号
            #     zd = Line.objects.filter(line_id=line_number)[0]
            #     dis = zd.line_mark
            # else:
            #     gid = order.order_property_set.all().values().order_by('goods_id')[0]['goods_id_id']
            #     sn = Goods.objects.filter(goods_id=gid)[0]
            #     dis = sn.goods_mark
            # 判断小车停的前后位置或者是让小车到点之后才发状态0
            # c = Ag.get()
            # lu = c.CalcDistance(c.FindPath(carr[0].car_mark+'_1', dis+'_1'))  # 计算是不是最小的距离
            #
            # car_list = [1, 2, 3, 4, 5]
            # car_list.pop(int(car_number) - 1)
            # car_lu = []
            # car_lu.append(lu)
            # for i in car_list:
            #     ca = Car.objects.all().get(car_number=i)
            #     print(ca)
            #     car_lu.append(c.CalcDistance(c.FindPath(ca.car_mark+'_1',dis+'_1')))
            #     print(c.CalcDistance(c.FindPath(ca.car_mark+'_1',dis+'_1')))
            # print(car_lu)
            # if lu == min(*car_lu):
            order.car_number = car
            order.save()
            print(car,'create ok')
            # 如果在取料点
            if carr.filter(car_mark__mark_id='1'):
                car.car_status = '3'
                car.save()
                # 站点号
                station_mark = order.station_id.station_mark.mark_id
                print('站点mark::' + station_mark)
                # 存入小车下一个目的地
                carr.update(distination=station_mark)

                #小车出发时的时候，取消当前点的占用状态
                Mark.objects.filter(mark_id=car.distination,line_id_id=line_id).update(mark_status='0')
                return HttpResponse(station_mark)
                # # 状态改为1
                # sta = Car_status.objects.all().get(number='1')
                # car.car_status = sta
                # car.save()
                # # 判断订单的工作类型，0表示送料，1表示送完成品
                # if Order.objects.get(order_status="未完成", car_number=car_number).work_type == '1':
                #     # 先去站点号
                #     line_number = order.line_id  # 线体号
                #     zd = Line.objects.filter(line_id=line_number)[0]
                #     print('先去站点' + zd.line_mark)
                #     # 存入小车下一个目的地
                #     carr.update(distination=zd.line_mark)
                #     return HttpResponse(zd.line_mark)
                # else:
                #     # 物料站点号
                #     gid = order.order_property_set.all().values().order_by('goods_id')[0]['goods_id_id']
                #     sn = Goods.objects.filter(goods_id=gid)[0]
                #     print('物料' + sn.goods_mark)
                #     # return HttpResponse()
                #     # 存入小车下一个目的地
                #     carr.update(distination=sn.goods_mark)
                #     return HttpResponse(sn.goods_mark)
            else:
                print('no')
                return HttpResponse()



        elif carr.filter(car_status='4'):

            car.car_status = '5'
            car.save()
            print('状态改为5', car.default_mark)
            # 存入小车下一个目的地
            Car.objects.filter(car_number=car_number).update(distination=car.default_mark)
            #小车出发时的时候，取消当前点的占用状态
            Mark.objects.filter(mark_id=car.distination,line_id_id=line_id).update(mark_status='0')
            return HttpResponse(car.default_mark)
        elif carr.filter(car_status='5'):

            print('no order')
            return HttpResponse('')
        else:
            car.car_status = '5'
            car.save()
            print('默认回到原点', car.default_mark)
            # 存入小车下一个目的地
            Car.objects.filter(car_number=car_number).update(distination=car.default_mark)
            #小车出发时的时候，取消当前点的占用状态
            Mark.objects.filter(mark_id=car.distination,line_id_id=line_id).update(mark_status='0')
            return HttpResponse(car.default_mark)



    elif int(status) == 2:
        # if pos:
        #     # 把小车现在的点取消，占用下一个点
        #     c = Ag.get()
        #     next_mark = c.FindNextPoint(pos + '_1', carr.values()[0]['distination'] + '_1')
        #     print(carr.values()[0]['distination'] + '_1', '目的地')
        #     # 如果随意移动了小车也要判断,
        #     # if Mark.objects.filter(mark_id=pos, mark_status='1'):
        #     #     Mark.objects.filter(mark_id=pos).update(mark_status='0')
        #     # else:
        #     #     next = c.FindNextPoint(carr.values()[0]['car_mark'] + '_1', carr.values()[0]['distination'] + '_1')
        #     #     Mark.objects.filter(mark_id=next[0:-2]).update(mark_status='0')
        #     print('当前点', pos, '下个点', next_mark)
        #     carr.update(car_mark=pos)
        #     # 查询下个点是否被占用
        #     if Mark.objects.filter(mark_id=next_mark[0:-2], mark_status='1'):
        #         return HttpResponse('停止')  # 小车收到这个表示要重复发送2，并且要停止
        #     Mark.objects.filter(mark_id=next_mark[0:-2]).update(mark_status='1')
        #
        #     return HttpResponse('走')  # 小车收到这个表示不用重复发，并且可以走
        # else:
        #     print('木有pos')
        list = ['64', '49', '34', '99', '37', '92', '40', '85', '78', '43', '71', '46']#待交汇的两个点
        meet = ['50', '47', '44', '41', '38', '35']#交汇点
        #存入当前位置
        mk=Mark.objects.get(mark_id=pos,line_id_id=line_id)
        carr.update(car_mark=mk)

        if pos in (list+meet):
            print('当前位置'+pos)
            if pos in meet:
                print('清除完毕')
                Mark.objects.filter(mark_id=pos,line_id_id=line_id).update(mark_status='0')
                return HttpResponse()
            else:
                # 查询下个点是否被占用
                next_m = mk.next_mark
                next = Mark.objects.get(mark_id=next_m,line_id_id=line_id)
                status = next.mark_status
                if status == '1':
                    print('停止')
                    return HttpResponse('停止')  # 小车收到这个表示要重复发送2，并且要停止
                next.mark_status = '1'
                next.save()
                print('通过save')
                return HttpResponse('走')  # 小车收到这个表示不用重复发，并且可以走
        else:
            print('不在合并处')
            return HttpResponse()



    elif int(status) == 4:
        Mark.objects.filter(mark_id=car.distination,line_id_id=line_id).update(mark_status='1')
        try:
            o=Order.objects.get(line_id_id=line_id,order_status="未完成", car_number=car)
        except:
            pass
        # 完成送料
        if carr.filter(car_status='3'):
            o.finish_time = tm
            o.order_status = '完成'
            # print(type(o.order_time))
            time_cha=my_time(tm,o.order_time)
            o.total_time = time_cha
            o.save()

            # 更改小车状态为4
            car.car_status = '4'
            car.save()
            #小车当前点更改为目的地点
            mk=Mark.objects.get(mark_id=car.distination,line_id_id=line_id)
            carr.update(car_mark=mk)
            print('送料完成')
            return HttpResponse('')
        elif carr.filter(car_status='1'):

            print('装料')

            # 两个以上时，修改物料点完成状态
            # orsn = o.order_property_set.filter(order_status='0').values().order_by('goods_id')[0]['id']
            #
            # Order_property.objects.filter(id=orsn, order_status='0').update(order_status='1')

            car.car_status ='2'
            car.save()
            #小车当前点更改为目的地点
            mk=Mark.objects.get(mark_id=car.distination,line_id_id=line_id)
            carr.update(car_mark=mk)
            return HttpResponse('taking')

        elif Car.objects.filter(car_number=car_number, car_status='5'):
            #小车当前点更改为目的地点
            mk=Mark.objects.get(mark_id=car.distination,line_id_id=line_id)
            carr.update(car_mark=mk)
            print('到达原点')
            return HttpResponse('')
        else:
            print('状态四错误')
            return HttpResponse('')
    else:
        print('return or send error')
        return HttpResponse('return')
