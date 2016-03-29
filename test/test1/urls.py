"""rob_test2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from app1.views import *

urlpatterns = [
    url(r'^material_request/$', material_request.material_request, name='material_request'),  # 提交订单
    url(r'^show_order/$', show_order.show_order, name='show_order'),  # 显示订单
    url(r'^end_order/$', end_order.end_order, name='end_order'),  # 完成订单
    url(r'^show_data/$', show_data.show_data, name='show_data'),  # ajax返回数据
    url(r'^show_car/$', show_car.show_car, name='show_car'),  # 显示小车路线
    url(r'^report_car_position/$', report_car_position.report_car_position, name='report_car_position'),  # 收集小车状态
    url(r'^reset/$', reset.reset, name='reset'),  # 恢复出厂设置
    url(r'^line_warn/$', line_warn.line_warn, name='line_warn'),  # 线体报警
    url(r'^display_warn/$', display_warn.display_warn, name='display_warn'),  # 显示历史告警服务请求记录
    url(r'^check_warn/$', check_warn.check_warn, name='check_warn'),  # 终端检查报警
    url(r'^admin/', admin.site.urls),
]
