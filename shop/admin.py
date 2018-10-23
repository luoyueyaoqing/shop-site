from django.contrib import admin
from .models import User, Product, Order, ShopCar, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['describe', 'price', 'count']
    list_filter = ['count']
    search_fields = ['describe']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'telphone', 'total_price', 'status']
    search_fields = ['user']
    list_per_page = 10


admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShopCar)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
