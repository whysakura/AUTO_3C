from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Order)
admin.site.register(Order_property)
admin.site.register(Line)
admin.site.register(Car)
admin.site.register(Station)
admin.site.register(Goods)
admin.site.register(Mark)
admin.site.register(Line_warn)
# admin.site.register(Error)