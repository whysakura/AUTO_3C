import time,datetime
#传入两个time.time()生成的时间戳
def my_time(t1,t2):
    t1=float(t1)
    t2=float(t2)
    li1=list(time.localtime(t1))[0:-3]
    li2=list(time.localtime(t2))[0:-3]
    if t1<t2:

        time_cha=datetime.datetime(*li2)-datetime.datetime(*li1)
    else:
        time_cha=datetime.datetime(*li1)-datetime.datetime(*li2)
    return time_cha

def timeTodatetime(t):
    t=float(t)
    li=time.localtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S',li)
# a=time.time()
# time.sleep(4)
# b=time.time()
# print(my_time(a,b))
# print(my_time(1458731307.29408,1451731289.840474))