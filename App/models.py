#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : models.py
# @Software: PyCharm

from django.db import models
# Create your models here.
from GPAXF.settings import no_pay


class HomeBaseModel(models.Model):
    """
    主页base model类
    """
    img = models.CharField(max_length=256)
    name = models.CharField(max_length=24)
    track_id = models.IntegerField(default=1)

    class Meta:
        abstract = True


class AxfHomeWheels(HomeBaseModel):
    """
    映射为主页轮播数据表
    """
    class Meta:
        db_table = 'axf_wheel'

    def __str__(self):
        return self.name


class AxfHomeNav(HomeBaseModel):
    """
    映射为主页导航数据表
    """
    class Meta:
        db_table = 'axf_nav'


class AxfHomeMustBuy(HomeBaseModel):
    """
    映射为主页必买数据表
    """
    class Meta:
        db_table = 'axf_must_buy'


class AxfShop(HomeBaseModel):
    """
    映射为主页商品表
    """
    class Meta:
        db_table = 'AxfShop'


class AxfHomeMainShow(HomeBaseModel):
    """
    映射为主页主要展示表
    """
    category_id = models.IntegerField(default=1)
    brand_name = models.CharField(max_length=24)
    img1 = models.CharField(max_length=128)
    child_cid1 = models.IntegerField(default=1)
    product_id1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=64)
    price1 = models.FloatField(default=1)
    market_price1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=128)
    child_cid2 = models.IntegerField(default=1)
    product_id2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=256)
    price2 = models.FloatField(default=1)
    market_price2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=256)
    child_cid3 = models.IntegerField(default=1)
    product_id3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=256)
    price3 = models.FloatField(default=1)
    market_price3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_main_show'


class MarketGoods(models.Model):
    """
    映射为超市商品表
    """
    product_id = models.IntegerField(default=1)
    product_img = models.CharField(max_length=256)
    product_name = models.CharField(max_length=24)
    product_long_name = models.CharField(max_length=48)
    isxf = models.BooleanField(default=1)
    pmdesc = models.BooleanField(default=1)
    specifics = models.FloatField(default=0)
    price = models.FloatField(default=0)
    market_price = models.FloatField(default=0)
    category_id = models.IntegerField(default=1)
    child_cid = models.IntegerField(default=1)
    child_cid_name = models.CharField(max_length=12)
    dealer_id = models.IntegerField(default=1)
    store_nums = models.IntegerField(default=1)
    product_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class GoodsType(models.Model):
    """
    映射为商品类型表
    """
    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=24)
    child_type_names = models.CharField(max_length=24)
    type_sort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_food_types'


class Goods(models.Model):
    """
    映射为商品表
    """
    g_name = models.CharField(max_length=20)


class Customs(models.Model):
    """
    映射为custom表
    """
    c_name = models.CharField(max_length=20)
    c_good = models.ManyToManyField(Goods)


class User(models.Model):
    """
    映射为用户表
    """
    user_account = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=20)
    user_icon = models.CharField(max_length=256)
    user_address = models.CharField(max_length=56)
    user_rank = models.IntegerField(default=1)
    user_token = models.CharField(max_length=50)
    if_activate = models.BooleanField(default=0)
    @classmethod
    def create_user(cln, accout, password, name, phone, icon, address, rank):
        return cln(user_account=accout, user_password=password, user_name=name,
                   user_phone=phone, user_icon=icon, user_adderss=address,
                   user_rank=rank)


class Cart(models.Model):
    """映射为购物车"""
    c_goods = models.ForeignKey(MarketGoods, on_delete=models.CASCADE)
    c_user = models.ForeignKey(User, on_delete=models.CASCADE)
    if_selected = models.BooleanField(default=True)
    goods_nums = models.IntegerField(default=1)


class Order(models.Model):
    """
    映射为订单表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    o_price = models.FloatField(default=0)
    o_status = models.IntegerField(default=no_pay)
    o_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.o_date)


class OrderGoods(models.Model):
    """
    映射为订单商品表
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    market_goods = models.ForeignKey(MarketGoods, on_delete=models.CASCADE)
    o_nums = models.IntegerField(default=1)
