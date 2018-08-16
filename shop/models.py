from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=32, null=True, blank=True)
    telphone = models.CharField(verbose_name="手机号码", max_length=11)
    address = models.CharField(verbose_name="邮寄地址", max_length=128)

    def __str__(self):
        return self.nickname or self.username


class Product(models.Model):
    pic = models.ImageField(upload_to="product_pic")
    describe = models.TextField()
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.describe[:20], self.price)


class ShopCar(models.Model):
    user = models.ForeignKey(to=User, related_name='shopcar')
    product = models.ForeignKey(to=Product, related_name='shopcars')
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}-{}'.format(self.user.username, self.product.id, self.count)


class Order(models.Model):
    user = models.ForeignKey(to=User, related_name='orders')
    telphone = models.CharField(max_length=11)
    create_time = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(default=0)
    address = models.CharField(max_length=128)
    STATUS = (
        ('wait', '待付款'),
        ('overdue', '已过期'),
        ('complete', '已完成'),
        ('refund', '已退款'),
    )
    status = models.CharField(max_length=9, choices=STATUS, default='wait')

    def __str__(self):
        return self.product.describe


class OrderProduct(models.Model):
    order = models.ForeignKey(to='Order', related_name="orders")
    product = models.ForeignKey(to=Product, related_name="orderproducts")
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.product.describe
