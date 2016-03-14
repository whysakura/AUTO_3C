# 3C车间设计





from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json, time, random
from itertools import chain
from django.core import serializers
from Agv import AgvCar
import sys
import threading


# Create your views here.
class Ag:
    c = AgvCar.AgvCar(r'.\Agv\3c_path\3c_agv_file', r'.\Agv\3c_path\turn.csv', r'.\Agv\3c_path\distance.csv')

    def get():
        return Ag.c
# 线体报警
def line_error(request):
    line_time=time.time()#时间
    data = json.loads(request.body.decode('utf-8'))
    line_id=data['line_id']#线体
    error_num=data['error_num']#报警号
    print(line_id,error_num,line_time)
    if error_num=='1':
        if Lineerror.objects.filter(line_id=line_id,line_state='1'):
            print('已经存在')
            return HttpResponse()
        line=Lineerror()
        line.line_id=line_id
        line.start_time=line_time
        line.line_state=error_num
        line.save()
    elif error_num=='2':
        Lineerror.objects.filter(line_id=line_id,line_state='1').update(line_state=error_num)
    else :
        Lineerror.objects.filter(line_id=line_id,line_state='2').update(line_state=error_num,over_time=line_time)
    return HttpResponse()

# 恢复出厂设置
def reset(request):
    for i in range(1, 100):
        m = Mark.objects.get(mark_id=str(i))
        m.mark_state = '0'
        m.save()
        print(m)
    for i in range(1, 6):
        car = Car.objects.get(car_number=str(i))
        sta = State.objects.all().get(sta_number='0')
        car.car_state = sta
        car.car_mark = ''
        car.default_mark = '1'
        car.distination = ''
        car.save()
    return HttpResponse()


# 创建订单号
def create_order():
    a = time.strftime('%Y%m%d%H%M%S')
    a = 'CIG3C_' + a
    items = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'q', 'w', 'e', 'r',
             't', 'y', 'u', 'i', 'p', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
    random.shuffle(items)
    num = a + str('').join(items)[0:5]
    if Order.objects.filter(order_sn=num):
        create_order()
    return num


def ask(request):
    data = json.loads(request.body.decode('utf-8'))
    or_num = create_order()
    line = data['0']['line']
    wtype = data['0']['type']
    if wtype == '1' and len(data) == 2:
        print('送完成品的只有一个点')
        return HttpResponse('error')
    if Order.objects.filter(line_id=line, order_state='未完成'):
        print('未完成')
        return HttpResponse('existed')
    for a, b in data.items():
        print(b['count'], b['line'], b['gid'])
        line = b['line']
        gid = b['gid']
        count = b['count']
        if line == '' or gid == '' or count == '':
            print('少参数')
            return HttpResponse('')
        # if Order.objects.all().count()>1000000:
        if not Order.objects.filter(order_sn=or_num):
            date = time.strftime('%Y/%m/%d %H:%M:%S')
            li_num = Linebody.objects.all().get(line_id=line)
            print(li_num)
            o = Order()
            o.line_id = li_num
            o.order_sn = or_num
            o.order_time = date
            o.work_type = wtype

            o.save()
            print('总订单数目' + str(Order.objects.all().count()))

        ordd = Order.objects.get(order_sn=or_num)
        goid = Goods.objects.get(goods_id=gid)
        o_de = Order_de()
        o_de.order_sn = ordd
        o_de.goods_id = goid
        o_de.goods_count = count
        o_de.save()
    return HttpResponse(or_num + '<br/>' + line + '<br/>' + date)


# 显示小车路线
def show_car(request):
    alldata = []
    for a in range(1, 6):
        # 返回所需数据
        lists = []
        lists.append(a)
        car = Car.objects.get(car_number=str(a))
        data = Car.objects.select_related().all().values(
            'car_state__sta_name',
            'car_mark',
            'distination',
        ).filter(car_number=str(a))
        lists.append(data[0]['car_state__sta_name'])
        if  data[0]['car_mark']:
            lists.append(data[0]['car_mark']+'号mark点')
        else:
            lists.append(data[0]['car_mark'])
        # lists.append(data[0]['distination'])
        d=data[0]['distination']
        if d=='':
            lists.append(data[0]['distination'])
        else:
            st=Linebody.objects.get(station_number=d).line_id
            if st=='0':
                st='取料点'
            else:
                st=st+'号站点'
            lists.append(st)
        # if car.order_set.filter(order_state='未完成'):
        # 	line_id=car.order_set.filter(order_state='未完成').values()[0]['line_id_id']
        # 	line_station=Linebody.objects.get(line_id=line_id).station_number
        # 	lists.append(line_station)
        # 	sn=car.order_set.filter(order_state='未完成').values()[0]['order_sn']
        # 	order=Order.objects.get(order_sn=sn)
        # 	gid=order.order_de_set.values().order_by('goods_id_id')
        # 	for x in gid:
        # 		gstation=Goods.objects.get(goods_id=x['goods_id_id']).goods_station
        # 		lists.append(gstation)
        # 		print(gstation)
        # 	print(lists)
        alldata.append(lists)
    print(alldata)
    if Mark.objects.filter(mark_state='1'):
        print(Mark.objects.filter(mark_state='1'))
    # 转换为jsonstr
    data = json.dumps(list(alldata), ensure_ascii=False)

    # json转为list
    # data=json.loads(data)
    # print(type(data))
    return HttpResponse(data)


# 显示完成订单
def over_order(request):
    data = Order_de.objects.select_related().all().values(
        'order_sn__line_id',
        'order_sn__order_sn',
        'order_sn__order_state',
        # 'order_sn__line_id__station_number',
        'order_sn__order_time',
        'order_sn__car_number',
        # 'order_sn__car_number__car_state__sta_name',
        # 'order_sn__work_type',
        'order_sn__finish_time',
        'order_sn__total_time',
        # 'goods_id',
        # 'goods_count',
        # 'goods_id__goods_name',
        # 'goods_id__goods_station',
    ).filter(order_sn__order_state='完成')
    return render(request, 'over.html', locals())


# 显示未完成订单
def show_order(request):
    data = Order_de.objects.select_related().all().values(
        'order_sn__line_id',
        'order_sn__order_sn',
        'order_sn__order_state',
        'order_sn__line_id__station_number',
        'order_sn__order_time',
        'order_sn__car_number',
        'order_sn__car_number__car_state__sta_name',
        # 'order_sn__work_type',
        # 'order_sn__finish_time',
        # 'order_sn__total_time',
        # 'goods_id',
        # 'goods_count',
        # 'goods_id__goods_name',
        # 'goods_id__goods_station',
    ).filter(order_sn__order_state='未完成')
    return render(request, 'show.html', locals())


# return HttpResponse(data)
# ajax数据
def show_data(request):
    data = Order_de.objects.select_related().all().values(
        'order_sn__line_id',
        'order_sn__order_sn',
        'order_sn__order_state',
        'order_sn__line_id__station_number',
        'order_sn__order_time',
        'order_sn__car_number',
        'order_sn__car_number__car_state__sta_name',
        # 'order_sn__work_type',
        # 'order_sn__total_time',
        # 'goods_id',
        # 'goods_count',
        # 'goods_id__goods_name',
        # 'goods_id__goods_type',
        # 'goods_id__goods_station',
    ).filter(order_sn__order_state='未完成')
    data = json.dumps(list(data),ensure_ascii=False)
    # print(data)
    return HttpResponse(data)


# 接受小车状态
def car_sta(request):
    car_data = json.loads(request.body.decode('utf-8'))
    state = car_data['car_state']
    num = car_data['car_number']
    if 'position' in car_data.keys():
        pos = car_data['position']
    print(car_data)
    carr = Car.objects.filter(car_number=num)

    tm = time.strftime('%Y/%m/%d %H:%M:%S')
    if int(state) == 0:
        Mark.objects.filter(mark_id=carr[0].car_mark).update(mark_state='0')
        # 判断是不是重复发送0
        if Order.objects.filter(order_state="未完成", car_number=num):
            order = Order.objects.filter(order_state="未完成", car_number=num).order_by('id')[0]
            # 返回站点代码
            if Car.objects.filter(car_number=num, car_state='3'):
                # 先判断是哪个工作类型
                if Order.objects.get(order_state="未完成", car_number=num).work_type == '1':
                    # 物料站点号
                    carr.update(distination='0x03')
                    print('再X去完成品地点0x03')
                    # 存入小车下一个目的地
                    carr.update(distination='0x03')
                    return HttpResponse('0x03')
                else:
                    # 站点号
                    line_number = order.line_id  # 线体号
                    zd = Linebody.objects.filter(line_id=line_number)[0]
                    print('站x点' + zd.station_number)
                    # 存入小车下一个目的地
                    carr.update(distination=zd.station_number)
                    return HttpResponse(zd.station_number)

                    # 如果重复发1，判断工作类型
            if Car.objects.filter(car_number=num, car_state='1'):
                # 返回站点
                if Order.objects.get(order_state="未完成", car_number=num).work_type == '1':
                    line_number = order.line_id  # 线体号
                    zd = Linebody.objects.filter(line_id=line_number)[0]
                    print('先去站点' + zd.station_number)
                    # 存入小车下一个目的地
                    carr.update(distination=zd.station_number)
                    return HttpResponse(zd.station_number)
                else:
                    # 物料站点号
                    gid = order.order_de_set.filter(order_state='0').values().order_by('goods_id')[0]['goods_id_id']
                    sn = Goods.objects.filter(goods_id=gid)[0]
                    print('物@料' + sn.goods_station)
                    # 存入小车下一个目的地
                    carr.update(distination=sn.goods_station)
                    return HttpResponse(sn.goods_station)

            if Car.objects.filter(car_number=num, car_state='2'):
                order = Order.objects.filter(car_number=num, order_state='未完成').order_by('id')[0]
                # 两个以上的物料点
                # if order.order_de_set.all().count()>1:
                # 	sta=State.objects.all().get(sta_number='1')
                # 	c=Car.objects.get(car_number=num)
                # 	c.car_state=sta
                # 	c.save()
                # 	orsn=order.order_de_set.all().values().order_by('goods_id')[0]['order_sn_id']
                # 	#查询未完成的物料点
                # 	if Order_de.objects.filter(order_sn=orsn,order_state='0'):
                # 		#物料站点号
                # 		gid=order.order_de_set.filter(order_state='0').values().order_by('goods_id')[0]['goods_id_id']
                # 		sn=Goods.objects.filter(goods_id=gid)[0]
                # 		print('物x料'+sn.goods_station)
                # 		#存入小车下一个目的地
                # 		carr.update(distination=sn.goods_station)
                # 		return HttpResponse(sn.goods_station)
                # 状态改为3
                sta = State.objects.all().get(sta_number='3')
                c = Car.objects.get(car_number=num)
                c.car_state = sta
                c.save()
                # 先判断是哪个工作类型
                if Order.objects.get(order_state="未完成", car_number=num).work_type == '1':
                    # 物料站点号
                    print('再X去完成品地点0x03')
                    # 存入小车下一个目的地
                    carr.update(distination='0x03')
                    return HttpResponse('0x03')
                else:
                    # 站点号
                    line_number = order.line_id  # 线体号
                    zd = Linebody.objects.filter(line_id=line_number)[0]
                    print('站x点' + zd.station_number)
                    # 存入小车下一个目的地
                    carr.update(distination=zd.station_number)
                    return HttpResponse(zd.station_number)


        # 分配任务
        elif Order.objects.filter(order_state="未完成", car_number=None) and carr[0].car_mark == '1':

            order = Order.objects.filter(order_state="未完成", car_number=None).order_by('id')[0]
            car = Car.objects.all().get(car_number=num)
            # if order.work_type == '1':  # 判断先去哪个目的地
            #     line_number = order.line_id  # 线体号
            #     zd = Linebody.objects.filter(line_id=line_number)[0]
            #     dis = zd.station_number
            # else:
            #     gid = order.order_de_set.all().values().order_by('goods_id')[0]['goods_id_id']
            #     sn = Goods.objects.filter(goods_id=gid)[0]
            #     dis = sn.goods_station
            # 判断小车停的前后位置或者是让小车到点之后才发状态0
            # c = Ag.get()
            # lu = c.CalcDistance(c.FindPath(carr[0].car_mark+'_1', dis+'_1'))  # 计算是不是最小的距离
            #
            # car_list = [1, 2, 3, 4, 5]
            # car_list.pop(int(num) - 1)
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
            print('create ok')
            # 如果在取料点
            if Car.objects.filter(car_number=num, car_mark='1'):
                sta = State.objects.all().get(sta_number='3')
                c = Car.objects.get(car_number=num)
                c.car_state = sta
                c.save()
                # 站点号
                line_number = order.line_id  # 线体号
                zd = Linebody.objects.filter(line_id=line_number)[0]
                print('站xx点' + zd.station_number)
                # 存入小车下一个目的地
                carr.update(distination=zd.station_number)
                return HttpResponse(zd.station_number)
                # 状态改为1
                sta = State.objects.all().get(sta_number='1')
                c = Car.objects.get(car_number=num)
                c.car_state = sta
                c.save()
                # 判断订单的工作类型，0表示送料，1表示送完成品
                if Order.objects.get(order_state="未完成", car_number=num).work_type == '1':
                    # 先去站点号
                    line_number = order.line_id  # 线体号
                    zd = Linebody.objects.filter(line_id=line_number)[0]
                    print('先去站点' + zd.station_number)
                    # 存入小车下一个目的地
                    carr.update(distination=zd.station_number)
                    return HttpResponse(zd.station_number)
                else:
                    # 物料站点号
                    gid = order.order_de_set.all().values().order_by('goods_id')[0]['goods_id_id']
                    sn = Goods.objects.filter(goods_id=gid)[0]
                    print('物料' + sn.goods_station)
                    # return HttpResponse()
                    # 存入小车下一个目的地
                    carr.update(distination=sn.goods_station)
                    return HttpResponse(sn.goods_station)
            else:
                print('no')
                return HttpResponse()



        elif Car.objects.filter(car_number=num, car_state='4'):
            sta = State.objects.all().get(sta_number='5')
            c = Car.objects.get(car_number=num)
            c.car_state = sta
            c.save()
            print('没有订单返回默认原点，状态改为5', c.default_mark)
            # 存入小车下一个目的地
            Car.objects.filter(car_number=num).update(distination=c.default_mark)
            return HttpResponse(c.default_mark)
        elif Car.objects.filter(car_number=num, car_state='5'):

            print('no order')
            return HttpResponse('')
        else:
            sta = State.objects.all().get(sta_number='5')
            c = Car.objects.get(car_number=num)
            c.car_state = sta
            c.save()
            print('默认回到原点', c.default_mark)
            # 存入小车下一个目的地
            Car.objects.filter(car_number=num).update(distination=c.default_mark)
            return HttpResponse(c.default_mark)



    elif int(state) == 2:
        # if pos:
        #     # 把小车现在的点取消，占用下一个点
        #     c = Ag.get()
        #     next_mark = c.FindNextPoint(pos + '_1', carr.values()[0]['distination'] + '_1')
        #     print(carr.values()[0]['distination'] + '_1', '目的地')
        #     # 如果随意移动了小车也要判断,
        #     # if Mark.objects.filter(mark_id=pos, mark_state='1'):
        #     #     Mark.objects.filter(mark_id=pos).update(mark_state='0')
        #     # else:
        #     #     next = c.FindNextPoint(carr.values()[0]['car_mark'] + '_1', carr.values()[0]['distination'] + '_1')
        #     #     Mark.objects.filter(mark_id=next[0:-2]).update(mark_state='0')
        #     print('当前点', pos, '下个点', next_mark)
        #     carr.update(car_mark=pos)
        #     # 查询下个点是否被占用
        #     if Mark.objects.filter(mark_id=next_mark[0:-2], mark_state='1'):
        #         return HttpResponse('停止')  # 小车收到这个表示要重复发送2，并且要停止
        #     Mark.objects.filter(mark_id=next_mark[0:-2]).update(mark_state='1')
        #
        #     return HttpResponse('走')  # 小车收到这个表示不用重复发，并且可以走
        # else:
        #     print('木有pos')
        list=['64','49','34','99','37','92','40','85','78','43','71','46']
        meet=['50','47','44','41','38','35']
        carr.update(car_mark=pos)
        if pos in list or list:
            if pos in meet:
                print('清除完毕')
                Mark.objects.filter(mark_id=pos).update(mark_state='0')
                return HttpResponse()
            else:
                # 查询下个点是否被占用
                next_m=Mark.objects.get(mark_id=pos).next_mark
                next=Mark.objects.get(mark_id=next_m)
                state=next.mark_state
                if state=='1':
                    print('1')
                    return HttpResponse('停止')  # 小车收到这个表示要重复发送2，并且要停止
                next.mark_state='1'
                next.save()
                print('save')
                return HttpResponse('走')  # 小车收到这个表示不用重复发，并且可以走
        else:
            print('不在合并处')
            return HttpResponse()



    elif int(state) == 4:
        c = Car.objects.get(car_number=num)
        Mark.objects.filter(mark_id=carr.values()[0]['distination']).update(mark_state='1')
        # 完成送料
        if Car.objects.filter(car_number=num, car_state='3'):
            o = Order.objects.get(car_number=num, order_state="未完成")
            # print(type(order))
            o.finish_time = tm
            o.order_state = '完成'
            # print(type(o.order_time))
            od = time.mktime(time.strptime(o.order_time, '%Y/%m/%d %H:%M:%S'))
            fi = time.mktime(time.strptime(tm, '%Y/%m/%d %H:%M:%S'))
            if float(fi - od) < 3600:
                fen = time.localtime(fi - od)
                time_cha = time.strftime('%M:%S', fen)
            elif float(fi - od) < 86400:
                fen = time.localtime(fi - od)
                time_cha = time.strftime('%H:%M:%S', fen)
            else:
                fen = time.localtime(fi - od)
                time_cha = time.strftime('%dd%H:%M:%S', fen)
            o.total_time = time_cha
            o.save()

            # 站位号
            sta = State.objects.all().get(sta_number='4')

            c.car_state = sta
            c.save()
            carr.update(car_mark=c.distination)
            print('送料完成')
            return HttpResponse('')
        elif Car.objects.filter(car_number=num, car_state='1'):
            o = Order.objects.get(car_number=num, order_state="未完成")
            # 放料时间
            # if Order.objects.filter(down_time=''):
            # 	o.down_time=tm
            o.save()
            print('装料')

            # 修改物料点完成状态
            orsn = o.order_de_set.filter(order_state='0').values().order_by('goods_id')[0]['id']

            Order_de.objects.filter(id=orsn, order_state='0').update(order_state='1')

            sta = State.objects.all().get(sta_number='2')

            c.car_state = sta
            c.save()
            carr.update(car_mark=c.distination)
            return HttpResponse('taking')

        elif Car.objects.filter(car_number=num, car_state='5'):
            carr.update(car_mark=c.distination)
            print('到达原点')
            return HttpResponse('')
        else:
            print('状态四错误')
            return HttpResponse('')
    else:
        print('return or send error')
        return HttpResponse('return')
