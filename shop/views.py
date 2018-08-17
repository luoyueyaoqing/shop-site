from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from .models import User, ShopCar, Product, OrderProduct, Order
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def index_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not User.objects.filter(username=username).exists():
            if password1 == password2:
                User.objects.create_user(username=username, password=password1)
                messages.success(request, '注册成功')
                return redirect(to='login')
            else:
                messages.warning(request, '两次密码输入不一致')
        else:
            messages.warning(request, "账号已存在")
    return render(request, 'shop_register.html')


def index_login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_url:
                return redirect(next_url)
            # return redirect('index')
            return HttpResponse('ok')
        return HttpResponseRedirect(request.get_full_path())
    return render(request, 'shop_login.html', {'next_url': next_url})


def index(request):
    products = Product.objects.all()
    return render(request, 'shop_list.html', {'products': products})


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
