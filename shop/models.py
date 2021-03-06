from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(verbose_name="昵称", max_length=32, null=True, blank=True)
    telphone = models.CharField(verbose_name="手机号码", max_length=11)
    address = models.CharField(verbose_name="邮寄地址", max_length=128)
    pic = models.ImageField(upload_to="user_pic", default="user_pic/IMG_0766.PNG")

    def __str__(self):
        return self.nickname or self.username


# # 自定义产品管理器,对于库存为 0 的不显示
# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(count__gt=0)


class Product(models.Model):
    pic = models.ImageField(upload_to="product_pic")
    describe = models.TextField()
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    # productmanager = ProductManager()

    def have_count(self):
        if self.count > 0:
            return True
        else:
            return False

    def del_count(self):
        if self.have_count():
            self.count -= 1
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return '{}'.format(self.describe[:20])


class ShopCar(models.Model):
    user = models.ForeignKey(to=User, related_name='shopcar')
    product = models.ForeignKey(to=Product, related_name='shopcars')
    count = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)

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
        return '{}-{}-{}'.format(self.user, self.total_price, self.status)


class OrderProduct(models.Model):
    order = models.ForeignKey(to='Order', related_name="orders")
    product = models.ForeignKey(to=Product, related_name="orderproducts")
    price = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.product.describe
