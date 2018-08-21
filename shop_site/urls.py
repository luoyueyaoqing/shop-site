from django.conf.urls import url
from django.contrib import admin
from shop import views
from django.views.static import serve
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.index_register, name='register'),
    url(r'^login/', views.index_login, name='login'),
    url(r'^logout/', views.index_logout, name='logout'),

    url(r'^user/', views.shop_user, name='shop_user'),
    url(r'^update_user/', views.update_user, name='update_user'),
    url(r'^index/', views.index, name='index'),
    url(r'^upload/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^shopcar/', views.shopcar, name='shopcar'),
    url(r'^add_shopcar/(?P<id>\d+)', views.add_shopcar, name='add_shopcar'),
    url(r'^del_shopcar/(?P<id>\d+)', views.del_shopcar, name='del_shopcar'),
    url(r'^delete_shopcar/(?P<shopcar_id>\d+)', views.delete_shopcar, name='delete_shopcar'),

    url(r'^generate/', views.generate, name='generate'),
    url(r'^generate_do/', views.generate_do, name='generate_do'),
    url(r'^pay/(?P<orderid>\d+)', views.pay, name='pay'),
    url(r'^order/', views.order, name='order'),
    url(r'^del_order/(?P<id>\d+)', views.del_order, name='del_order'),
]
