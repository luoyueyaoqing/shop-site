from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from .models import User, ShopCar, Product, OrderProduct, Order
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.cache import cache_page


def index_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        code1 = request.POST.get('code1')
        code2 = request.session.get('code')
        if code1 == code2:
            if not User.objects.filter(username=username).exists():
                if password1 == password2:
                    User.objects.create_user(username=username, password=password1)
                    messages.success(request, '注册成功')
                    return redirect(to='login')
                else:
                    messages.warning(request, '两次密码输入不一致')
            else:
                messages.warning(request, "账号已存在")
        else:
            messages.warning(request, '验证码输入错误')
    return render(request, 'shop_register.html')


def index_login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_url:
                return redirect(next_url)
            return redirect('index')
        return HttpResponseRedirect(request.get_full_path())
    return render(request, 'shop_login.html', {'next_url': next_url})


def index_logout(request):
    logout(request)
    return redirect(to='index')


@login_required
def shop_user(request):
    user = request.user
    return render(request, 'shop_user.html', {'user': user})


@login_required
def update_user(request):
    user = request.user
    if request.method == "POST":
        user.nickname = request.POST.get('nickname')
        user.telphone = request.POST.get('telphone')
        user.address = request.POST.get('address')
        user.save()
        return redirect(to='shop_user')
    return render(request, 'update_user.html', {'user': user})


# @cache_page(60 * 10)
def index(request):
    # from random import randint
    # for i in range(50):
    #     product = Product.objects.create(pic="product_pic/IMG_0766.PNG", describe="product--{}".format(i*i), price=randint(20, 200), count=randint(5, 50))
    products = Product.objects.all()
    paginator = Paginator(products, 8)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        product_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'shop_list.html', {'product_list': product_list})


@login_required
def shopcar(request):
    shopcar = ShopCar.objects.filter(user=request.user)
    return render(request, 'shop_car.html', {'shopcar': shopcar})


@login_required
def add_shopcar(request, id):
    product = Product.objects.get(id=id)
    product.count -= 1
    shopcar, status = ShopCar.objects.get_or_create(user=request.user, product=product)
    shopcar.count += 1
    shopcar.total_price = shopcar.count * shopcar.product.price
    shopcar.save()
    return redirect('/shopcar/')


@login_required
def del_shopcar(request, id):
    shopcar = ShopCar.objects.get(id=id)
    shopcar.count -= 1
    if shopcar.count < 1:
        shopcar.delete()
    else:
        shopcar.total_price = shopcar.count * shopcar.product.price
        shopcar.save()
    return redirect(to='shopcar')


@login_required
def delete_shopcar(request, shopcar_id):
    shopcar = ShopCar.objects.get(id=shopcar_id)
    shopcar.delete()
    return redirect(to='shopcar')


@login_required
def generate(request):
    shopcar = ShopCar.objects.filter(user=request.user)
    all_price = sum([sc.total_price for sc in shopcar])
    return render(request, 'shop_generate_order.html', {'shopcar': shopcar, 'all_price': all_price})


@login_required
def generate_do(request):
    shopcar = ShopCar.objects.filter(user=request.user)
    if not shopcar:
        return redirect(to='index')
    all_price = sum([sc.total_price for sc in shopcar])
    order = Order.objects.create(user=request.user, telphone=request.user.telphone, address=request.user.address,
                                 total_price=all_price)
    order.save()
    for sc in shopcar:
        orderproduct = OrderProduct(order=order, product=sc.product, price=sc.product.price, count=sc.count,
                                    total_price=sc.total_price)
        orderproduct.save()
        sc.delete()
        return redirect(to='pay', orderid=order.id)


@login_required
def pay(request, orderid):
    order = Order.objects.filter(user=request.user, id=orderid, status="wait")
    if not order.exists():
        order = None
    else:
        order = order.first()
    check_status = request.GET.get('check')
    if check_status and order:
        if check_status == "pay":
            order.status = "complete"
            [orderprodduct.product.del_count() for orderprodduct in order.orders.all()]
        elif check_status == "cancel":
            order.status = "overdue"
        order.save()
        return redirect(to="order")
    return render(request, 'shop_pay.html', {'order': order})


@login_required
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop_order.html', {'orders': orders})


@login_required
def del_order(request, id):
    order = Order.objects.get(user=request.user, id=id)
    order.delete()
    return redirect(to='order')


# 验证码
def verifyCode(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 创建背景色,宽,高
    bgColor = (random.randrange(30, 100), random.randrange(30, 100), 0)
    width = 100
    height = 25
    # 创建画布
    image = Image.new('RGB', (width, height), bgColor)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 创建文本内容
    text = '0123456789ABCDEFG'
    # 逐个绘制文本内容
    textTemp = ''
    for i in range(4):
        text1 = text[random.randrange(0, len(text))]
        textTemp += text1
        draw.text((i * 25, 5),
                  text1,
                  fill=fontcolor)
    request.session['code'] = textTemp
    # 保存到内存流中
    from io import BytesIO
    buf = BytesIO()
    image.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
