#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : views_helper.py
# @Software: PyCharm

import hashlib
import time

from App.models import Cart


class HelperMixin:
    """
    帮助函数类

    主要是为了给view创建一些功能性的函数，主要有生成token，得到购物车的总价...
    """

    def get_total_price(self):
        """
        功能性函数：返回购 物车总价
        :return total_price:
        """
        total_price = 0
        for i in Cart.objects.all():
            if i.if_selected:
                total_price = total_price + i.goods_nums * i.c_goods.price
        total_price = '{:.2f}'.format(total_price)
        return total_price

    def create_token(self, user_account):
        """
        功能性函数，创建一个token，用于会话技术和激活账号
        """
        a = hashlib.md5()
        a.update((user_account + str(time.time())).encode('utf-8'))
        return a.hexdigest()
