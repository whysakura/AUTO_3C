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
from app1 import views as gd_views

urlpatterns = [
    url(r'^ask/$', gd_views.ask, name='ask'),  # 提交订单
    url(r'^show_order/$', gd_views.show_order, name='show_order'),  # 显示订单
    url(r'^over_order/$', gd_views.over_order, name='over_order'),  # over订单
    url(r'^show_data/$', gd_views.show_data, name='show_data'),  # ajax返回数据
    url(r'^show_car/$', gd_views.show_car, name='show_car'),  # 显示小车路线
    url(r'^car_sta/$', gd_views.car_sta, name='car_sta'),  # 收集小车状态
    url(r'^test/$', gd_views.test),  # 恢复出厂设置
    url(r'^ensure/$', gd_views.ensure),  # 确定订单
    url(r'^delete_order/$', gd_views.delete_order),  # 订单取消
    url(r'^line_error/$', gd_views.line_error),  # 线体报警
    url(r'^admin/', admin.site.urls),
]
