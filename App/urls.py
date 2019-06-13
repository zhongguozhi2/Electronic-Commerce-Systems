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
    url(r'^HomeVIew/$', views.HomeView.as_view(), name='HomeVIew'),
    # 商品展示路由
    url(r'^market$', views.market, name='market'),
    url(r'^MarketWithArgs/(?P<category_id>\d+)/(?P<child_cid>\d+)/(?P<sort_mode>\d+)',
        cache_page(60 * 2)(views.MarketWithArgsView.as_view()), name='MarketWithArgs'),
    # 购物车路由
    url(r'^CartPage/$', views.CartView.as_view(), name='CartPage'),
    url(r'^ChangeCart/(?P<operation>\d)/$',
        views.ChangeCartView.as_view(), name='ChangeCart'),
    url(r'^ChangeStatus/$',
        views.ChangeStatusView.as_view(),
        name='ChangeStatus'),
    url(r'^ChangeAllStatus/$',
        views.ChangeAllStatusView.as_view(),
        name='ChangeAllStatus'),
    url(r'^ChangeCartNum/$',
        views.ChangeCartNumView.as_view(),
        name='ChangeCartNum'),
    # 个人中心路由
    url(r'^Register/$', views.RegisterView.as_view(), name='Register'),
    url(r'^CheckUserId/$', views.CheckUserIdView.as_view(), name='CheckUserId'),
    url(r'^Login/$', views.Login.as_view(), name='Login'),
    url(r'^Mine/$', views.MineView.as_view(), name='Mine'),
    url(r'^Quit/$', views.QuitView.as_view(), name='Quit'),
    url(r'^out/$', views.out, name='out'),
    url(r'^Activate/', views.ActivateView.as_view(), name='Activate'),
    # 订单路由
    url(r'^AddOrder/$', views.AddOrderView.as_view(), name='AddOrder'),
    url(r'^OrderAjax/$', views.OrderAjaxView.as_view(), name='OrderAjax')
]
