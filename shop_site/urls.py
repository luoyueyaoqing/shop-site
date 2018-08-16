from django.conf.urls import url
from django.contrib import admin
from shop import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.index_register, name='register'),
    url(r'^login/', views.index_login, name='login'),
]
