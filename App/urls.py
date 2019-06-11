#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [

    # 主页路由
    url(r'^Home/$', views.Home.as_view(), name='Home'),
    # 商品展示路由
    url(r'^market$', views.market, name='market'),
    url(r'^MarketWithArgs/(?P<category_id>\d+)/(?P<child_cid>\d+)/(?P<sort_mode>\d+)',
        cache_page(60 * 2)(views.MarketWithArgs.as_view()), name='MarketWithArgs'),
    # 购物车路由
    url(r'^CartPage/$', views.CartPage.as_view(), name='CartPage'),
    url(r'^ChangeCart/(?P<operation>\d)/$',
        views.ChangeCart.as_view(), name='ChangeCart'),
    url(r'^ChangeStatus/$', views.ChangeStatus.as_view(), name='ChangeStatus'),
    url(r'^ChangeAllStatus/$',
        views.ChangeAllStatus.as_view(),
        name='ChangeAllStatus'),
    url(r'^ChangeCartNum/$',
        views.ChangeCartNum.as_view(),
        name='ChangeCartNum'),
    # 个人中心路由
    url(r'^Register/$', views.Register.as_view(), name='Register'),
    url(r'^CheckUserId/$', views.CheckUserId.as_view(), name='CheckUserId'),
    url(r'^Login/$', views.Login.as_view(), name='Login'),
    url(r'^Mine/$', views.Mine.as_view(), name='Mine'),
    url(r'^Quit/$', views.Quit.as_view(), name='Quit'),
    url(r'^out/$', views.out, name='out'),
    url(r'^Activate/', views.Activate.as_view(), name='Activate'),
    # 订单路由
    url(r'^AddOrder/$', views.AddOrder.as_view(), name='AddOrder'),
    url(r'^OrderAjax/$', views.OrderAjax.as_view(), name='OrderAjax')
]
