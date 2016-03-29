from django.db import models


# Create your models here.

# 错误警报
class Error(models.Model):
    error_id = models.CharField(primary_key=True, max_length=40)
    error_type = models.CharField(max_length=40)
    error_name = models.CharField(max_length=40)

# 线体
class Line(models.Model):
    line_id = models.CharField(primary_key=True, max_length=40)  # 车间号
    Description=models.CharField(max_length=120,default='')  #详细描述
    def __str__(self):
        return self.line_id



# mark点
class Mark(models.Model):
    line_id = models.ForeignKey(Line, blank=True, null=True)  # 外键车间号
    mark_id = models.CharField(max_length=30)
    mark_status = models.CharField(max_length=30, default='0')  # 占用状态，默认0没有占用
    next_mark = models.CharField(max_length=30, default='')

    class Meta:
        ordering = ['mark_id']

    def __str__(self):
        return 'Mark:'+str(self.line_id)+self.mark_id


# 站点
class Station(models.Model):
    station_id = models.CharField(max_length=50)
    station_mark = models.ForeignKey(Mark, blank=True, null=True)
    def __str__(self):
        return 'Station:'+str(self.station_mark.line_id_id)+self.station_id

# 线体报警
class Line_warn(models.Model):
    line_id = models.ForeignKey(Line, blank=True, null=True)  # 车间号
    line_station = models.ForeignKey(Station, blank=True,null=True,default='')  # 站点
    line_status = models.CharField(max_length=40, default='0')  # 线体报警状态
    start_time = models.CharField(max_length=40, default='')  # 请求时间
    end_time = models.CharField(max_length=40, default='')  # 请求时间
    total_time = models.CharField(max_length=40, default='')  # 总时间

    def __str__(self):
        return 'Line_warn:'+self.line_id_id + str(self.line_station)

# 物料
class Goods(models.Model):
    goods_line = models.ForeignKey(Line, blank=True, null=True,default='')  # 车间号
    goods_id = models.CharField(max_length=40,primary_key=True)
    goods_name = models.CharField(max_length=40)
    goods_type = models.CharField(max_length=40)
    goods_station = models.ForeignKey(Station, blank=True, null=True)  # 物料站点号
    goods_counts = models.IntegerField(default=0)  # 总数

    def __str__(self):
        return 'Goods:'+self.goods_line_id+self.goods_id


# 小车
class Car(models.Model):
    CAR_STATUS_CHOICES=(
        ('0','空置'),
        ('1', '取料'),
        ('2', '装料'),
        ('3', '送料'),
        ('4', '完成'),
        ('5', '无任务返回原点'),
    )
    car_number = models.CharField(max_length=40)  # 名称
    line_id=models.ForeignKey(Line,blank=True,null=True) #小车属于哪个车间
    car_status = models.CharField(max_length=10,choices=CAR_STATUS_CHOICES,default='0')  # 状态
    car_mark = models.ForeignKey(Mark, blank=True, null=True)  # 当前mark
    default_mark = models.CharField(max_length=40, default='')  # 默认停放点
    distination = models.CharField(max_length=40, default='', blank=True)  # 下一个目的地

    def __str__(self):
        return 'Car:'+str(self.line_id)+self.car_number


# 订单
class Order(models.Model):
    order_sn = models.CharField(max_length=40)  # 订单号
    line_id=models.ForeignKey(Line,blank=True,null=True) #小车属于哪个车间
    station_id = models.ForeignKey(Station,blank=True,null=True)  # 站点号
    order_time = models.CharField(max_length=40)  # 创建时间
    order_status = models.CharField(max_length=40, default='未完成')  # 状态
    car_number = models.ForeignKey(Car, blank=True, null=True)  # 小车号
    different_car=models.CharField(max_length=40,default='', blank=True)#区别小车
    finish_time = models.CharField(max_length=40, default='', blank=True)  # 完成时间
    total_time = models.CharField(max_length=40, default='', blank=True)  # 总时间
    work_type = models.CharField(max_length=40, default='', blank=True)  # 工作类型，0表示送料，1表示送完成品

    def __str__(self):
        return 'Order:'+self.order_sn


# 订单详情
class Order_property(models.Model):
    order_sn = models.ForeignKey(Order)  # 订单号
    goods_id = models.ForeignKey(Goods)  # 商品号
    order_count = models.IntegerField(default=0)  # 商品数
    order_status = models.CharField(max_length=40, default='0')

    def __str__(self):
        return 'Order_property:'+str(self.order_sn)
