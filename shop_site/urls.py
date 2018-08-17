from django.conf.urls import url
from django.contrib import admin
from shop import views
from django.views.static import serve
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.index_register, name='register'),
    url(r'^login/', views.index_login, name='login'),

    url(r'^index/', views.index, name='index'),
    url(r'^upload/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^shopcar/', views.shopcar, name='shopcar'),
    url(r'^add_shopcar/(?P<id>\d+)', views.add_shopcar, name='add_shopcar'),
    url(r'^del_shopcar/(?P<id>\d+)', views.del_shopcar, name='del_shopcar'),
]
