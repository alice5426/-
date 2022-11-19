from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=4, null=True)
    phone_number = models.CharField(max_length=11, null=True)
    create_time = models.DateTimeField(null=True)
    modifytime = models.DateTimeField(null=True)


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


class Cart(models.Model):
    user_id = models.BigIntegerField(null=False, default=1)
    goods_id = models.BigIntegerField(null=False, default=1)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    modify_time = models.DateTimeField(null=True, auto_now_add=True)


class Sort(models.Model):
    sort_name = models.CharField(max_length=255, null=False)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    modify_time = models.DateTimeField(null=True, auto_now_add=True)

