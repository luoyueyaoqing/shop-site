from django.contrib import admin
from .models import User, Product, Order, ShopCar, OrderProduct


admin.site.register(User)
admin.site.register(Product)
admin.site.register(ShopCar)
admin.site.register(Order)
admin.site.register(OrderProduct)

