"""Project_one URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/classify/', views.classify),
    path('index/recover/', views.database_back_up),
    # 测试
    path('test/', views.test),
    path('login/', views.login),
    path('register/', views.register),
    path('login_out/', views.login_out),
    path('404/',views.error_404),

    path('user_center/', views.user_center),
    path('user_center/del_good/', views.del_goods),
    path('user_center/del_cart/', views.del_carts),
    path('user_center/buy_good/', views.buy_goods),
    path('user_center/del_buy/', views.del_buys),
    path('user_center/user_information/', views.users_information),

    path('index/issue_page/', views.issue_page),
    path('index/issue_page/issue_form/', views.issue_form),

    path('goods_detail_page/', views.good_detail_page),
    path('goods_detail_page/join_cart/', views.join_cart),
    re_path(r'goods_detail_page?id=(\d+)', views.good_detail_page),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
