from django.db import models


# Create your models here.

# 错误警报
class Error(models.Model):
    error_id = models.CharField(primary_key=True, max_length=40)
    error_type = models.CharField(max_length=40)
    error_name = models.CharField(max_length=40)


# 线体报警
class Lineerror(models.Model):
    line_id = models.CharField(max_length=40)  # 线体号
    line_state = models.CharField(max_length=40)  # 线体报警状态
    line_time = models.CharField(max_length=40,default='0')  # 请求时间
    def __str__(self):
        return self.line_id

# 线体
class Linebody(models.Model):
    line_id = models.CharField(primary_key=True, max_length=40)  # 线体号
    station_number = models.CharField(max_length=40)  # 站点号
    def __str__(self):
        return self.line_id


# 物料
class Goods(models.Model):
    goods_id = models.CharField(primary_key=True, max_length=40)
    goods_name = models.CharField(max_length=40)
    goods_type = models.CharField(max_length=40)
    goods_station = models.CharField(max_length=40, default='')  # 物料站点号

    def __str__(self):
        return self.goods_id


# 状态号
class State(models.Model):
    sta_number = models.CharField(max_length=30, primary_key=True)
    sta_name = models.CharField(max_length=30)
    line_error = models.CharField(max_length=40, default='0')  # 线体报警

    def __str__(self):
        return self.sta_number


# mark点
class Mark(models.Model):
    mark_id = models.CharField(max_length=30, primary_key=True)
    mark_state = models.CharField(max_length=30, default='0')  # 占用状态，默认0没有占用

    class Meta:
        ordering = ['mark_id']

    def __str__(self):
        return self.mark_id


# 小车
class Car(models.Model):
    car_number = models.CharField(max_length=40, primary_key=True)  # 名称
    car_state = models.ForeignKey(State)  # 状态
    car_mark = models.CharField(max_length=40, blank=True, default='')  # mark
    default_mark = models.CharField(max_length=40, default='')  # 默认停放点
    distination = models.CharField(max_length=40, default='', blank=True)  # 下一个目的地

    def __str__(self):
        return self.car_number


# 订单
class Order(models.Model):
    order_sn = models.CharField(max_length=40)  # 订单号
    line_id = models.ForeignKey(Linebody)  # 线体号
    order_time = models.CharField(max_length=40)  # 创建时间
    order_state = models.CharField(max_length=40, default='未完成')  # 状态
    car_number = models.ForeignKey(Car, blank=True, null=True)  # 小车号
    # different_car=models.CharField(max_length=40,default='0')#区别小车
    finish_time = models.CharField(max_length=40, default='', blank=True)  # 完成时间
    total_time = models.CharField(max_length=40, default='', blank=True)  # 总时间
    work_type = models.CharField(max_length=40, default='', blank=True)  # 工作类型，0表示送料，1表示送完成品

    def __str__(self):
        return self.order_sn


# 订单详情
class Order_de(models.Model):
    order_sn = models.ForeignKey(Order)  # 订单号
    goods_id = models.ForeignKey(Goods)  # 商品号
    goods_count = models.IntegerField(default='')  # 商品数
    order_state = models.CharField(max_length=40, default='0')

    def __str__(self):
        return str(self.order_sn)


# 订单
class OrderPcb(models.Model):
    order_sn = models.CharField(max_length=40)  # 订单号
    line_id = models.ForeignKey(Linebody)  # 线体号
    order_time = models.CharField(max_length=40)  # 创建时间
    order_state = models.CharField(max_length=40, default='未完成')  # 状态
    car_number = models.ForeignKey(Car, blank=True, null=True)  # 小车号
    finish_time = models.CharField(max_length=40, default='', blank=True)  # 完成时间
    total_time = models.CharField(max_length=40, default='', blank=True)  # 总时间
    work_type = models.CharField(max_length=40, default='', blank=True)  # 工作类型，0表示送料，1表示送完成品

    def __str__(self):
        return self.order_sn


# 订单详情
class OrderPcb_de(models.Model):
    order_sn = models.ForeignKey(OrderPcb)  # 订单号
    goods_id = models.ForeignKey(Goods)  # 商品号
    goods_count = models.IntegerField(default='')  # 商品数
    order_state = models.CharField(max_length=40, default='0')

    def __str__(self):
        return str(self.order_sn)
