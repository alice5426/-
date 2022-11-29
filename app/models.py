from django.db import models


# 用户表
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=4, null=True)
    phone_number = models.CharField(max_length=11, null=True)
    img = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    information = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    modifytime = models.DateTimeField(null=True, auto_now_add=True)


# 发布商品表
class Goods(models.Model):
    img = models.CharField(max_length=255, null=True)
    sort_id = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    name = models.CharField(max_length=255, null=True)
    detal = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    modify_time = models.DateTimeField(null=True, auto_now_add=True)
    user_id = models.IntegerField()
    master_pho = models.CharField(max_length=255, null=True)


# 存放购买的商品（购物车）
class Cart(models.Model):
    cart_user_id = models.BigIntegerField(null=False, default=1)
    goods_id = models.BigIntegerField(null=False, default=1)
    cart_create_time = models.DateTimeField(null=True, auto_now_add=True)
    cart_modify_time = models.DateTimeField(null=True, auto_now_add=True)


# 商品分类名称的表
class Sort(models.Model):
    sort_name = models.CharField(max_length=255, null=False)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    modify_time = models.DateTimeField(null=True, auto_now_add=True)


# 购买商品表
class Buy(models.Model):
    user_id = models.BigIntegerField(null=False, default=1)
    good_id = models.BigIntegerField(null=False, default=1)
    create_time = models.DateTimeField(null=True, auto_now_add=True)