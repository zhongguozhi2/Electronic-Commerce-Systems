#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : view.py
# @Software: PyCharm

import os
import uuid
import hashlib

from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, ListView, DetailView, RedirectView
from App.views_helper import HelperFun
from GPAXF import settings
from GPAXF.settings import COMPREHENSIVE_ORDER, SALES_QUANTITY_ORDER, PRICE_ASE_ORDER, \
    PRICE_DESC_ORDER, ADD_OPERATION, SUB_OPERATION, NOT_ALL_STATUS, ALL_STATUS
from .models import *
# Create your views here.


# 方法装饰器，指定装饰dispatch方法，可以应用到类，因为不管是什么类型的请求，都会走先走dispatch方法
@method_decorator(cache_page(60), name='dispatch')
class Home(ListView):
    """主页

    展示项目的主要信息，包括：轮播展示部分热卖商品，商品导航栏，必买商品和超市
    """
    model = AxfHomeWheels
    template_name = 'main/Home.html'

    def get_queryset(self):
        self.title = '主页'
        self.wheel_datas = AxfHomeWheels.objects.all()
        self.nav_datas = AxfHomeNav.objects.all()
        self.must_buy_datas = AxfHomeMustBuy.objects.all()
        self.shop_datas = AxfShop.objects.all()
        self.shop0_1_datas = self.shop_datas[0:1]  # 取出闪送超市对象
        self.shop1_3_datas = self.shop_datas[1:3]  # 取出热卖商品对象
        self.shop3_7_datas = self.shop_datas[3:7]  # 取出分类商品对象
        self.shop7_11_datas = self.shop_datas[7:11]  # 取出超市商品对象
        self.mainshow_datas = AxfHomeMainShow.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        context['nav_datas'] = self.nav_datas
        context['wheel_datas'] = self.wheel_datas
        context['must_buy_datas'] = self.must_buy_datas
        context['shop0_1_datas'] = self.shop0_1_datas
        context['shop1_3_datas'] = self.shop1_3_datas
        context['shop3_7_datas'] = self.shop3_7_datas
        context['shop7_11_datas'] = self.shop7_11_datas
        context['mainshow_datas'] = self.mainshow_datas
        return context

# 方法装饰器，指定装饰dispatch方法，可以应用到类，因为不管是什么类型的请求，都会走先走dispatch方法
@method_decorator(cache_page(60), name='dispatch')
class MarketWithArgs(View):
    """商品展示页面

    展示项目的全部商品，根据不同的类别展示不同的商品，用户可以选择不同的排序方式，包括：综合排序
    销量排序，价钱高低排序等
    """
    model = MarketGoods
    template_name = 'main/market.html'

    def get(self, request, category_id, child_cid, sort_mode):
        category_id = int(category_id)
        child_cid = int(child_cid)
        sort_mode = int(sort_mode)
        type_datas = GoodsType.objects.all()
        goods_type_datas = MarketGoods.objects.filter(category_id=category_id)
        child_category_datas = [j for j in [i.split(':')  # 列表生成式方法取出子类的数据
                                            for i in GoodsType.objects.filter
                                            (typeid=category_id)[0].childtypenames.split('#')]]
        goods_by_cid_datas = goods_type_datas.filter(child_cid=child_cid)
        title = '闪购'
        if child_cid is COMPREHENSIVE_ORDER:  # 综合排序
            goods_datas = goods_type_datas
        else:
            goods_datas = goods_by_cid_datas
        if sort_mode is SALES_QUANTITY_ORDER:  # 按销售数量排序
            goods_datas = goods_datas.order_by("product_num")
        if sort_mode is PRICE_ASE_ORDER:  # 按价格升序排序
            goods_datas = goods_datas.order_by("price")
        if sort_mode is PRICE_DESC_ORDER:  # 按价格降序排序
            goods_datas = goods_datas.order_by("-price")
        context = {
            'title': title,
            'category_id': category_id,
            'child_cid': child_cid,
            'type_datas': type_datas,
            'goods_type_datas': goods_type_datas,
            'child_category_datas': child_category_datas,
            'goods_datas': goods_datas,
            'sort_mode': sort_mode,
        }
        return render(request, 'main/market.html', context=context)


# 登陆界面
class Login(LoginView):
    template_name = 'user/Login.html'

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)


class Register(View):
    """注册账号页面

    用户可以在这个页面注册账号
    ps：后端已完成，前端开发一部分，后面打算用vue来完善
    """

    def get(self, request):
        context = {
            'title': '注册',
        }
        return render(request, 'user/Register.html', context)

    def post(self, request):
        user_account = request.POST['userAccount']
        user_password = request.POST['userPassword']
        hash_password = hashlib.md5(
            (user_password + 'salt').encode('utf-8')).hexdigest()
        user_name = request.POST['userName']
        user_phone = request.POST['userPhone']
        user_address = request.POST['userAddress']
        user_icon = request.FILES['userIcon']
        user_icon1 = os.path.join(settings.MDEIA_ROOT, user_account + '.png')
        with open(user_icon1, "wb") as fp:
            for i in user_icon.chunks():
                fp.write(i)
        user_rank = 1
        User.createUser(user_account, hash_password, user_name, user_phone,
                        user_icon1, user_address, user_rank).save()
        token = uuid.uuid4().hex  # uuid生成一个永不相等的随机字符串
        cache.set('token', token, 24 * 60 * 60)
        activate_template = loader.get_template('user/email.html').\
            render({'userAccount': user_account, 'token': token})
        # 发送邮件激活账号，这里用的是网易邮箱，后面可分离出来，加入其他激活方式
        send_mail(
            subject='Activate axf',
            message='hello',
            from_email='xiaozhizhi_0@163.com',
            recipient_list=[
                'xiaozhizhi_0@163.com',
            ],
            html_message=activate_template)
        response = redirect(reverse('App:Mine'))
        return response


class Quit(RedirectView):
    """
    退出登陆,之后重定向到个人中心界面
    """
    url = '/App/Mine/'
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(Quit, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Quit, self).get(request, *args, **kwargs)


class CheckUserId(View):
    """
    在用户注册账号的时候检查用户名是否已经注册过了，使用的技术是ajax预校验
    """

    def post(self, request):
        user_id = request.POST.get("user_id")
        try:
            User.objects.get(userAccount=user_id)
            return JsonResponse({"data": "改用户已经被注册", "status": "error"})
        except User.DoesNotExist:
            return JsonResponse({"data": "可以注册", "status": "success"})


class Mine(DetailView):
    """ 用户的个人中心展示界面

    展示用户的信息，目前只展示了用户的用户名、头像等基本信息，后面添加更多有用的信息
    """
    model = User
    template_name = 'main/Mine.html'

    def get(self, request, *args, **kwargs):
        try:
            request_token = request.session.get('tok')  # 验证token
            user = User.objects.get(userToken=request_token)
        except User.DoesNotExist:
            return redirect("/App/Login/")
        else:
            self.username = user.userName

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['username'] = self.username
        context['title'] = '我的'


class CartPage(HelperFun, ListView):
    """购物车页面

    这个页面展示用户在market_with_args页面添加的商品，显示的主要有用户的信
    息、地址、购物车商品，用户在这个页面
    还可以增加和删除购物的商品，和一个添加为订单的按钮，生成订单
    """
    model = Cart
    template_name = 'main/Cart.html'

    def get_queryset(self):
        self.carts = Cart.objects.all()
        if Cart.objects.filter(if_selected=False).exists():
            self.if_all_select = False
        else:
            self.if_all_select = True
        self.total_price = super().get_total_price()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['total_price'] = self.total_price
        context['if_all_select'] = self.if_all_select
        context['carts'] = self.carts
        context['title'] = '购物车'
        return context


class Activate(View):
    """激活账号

    通过发送邮箱的方式激活已经注册好的账号
    ps：目前提供的是网易邮箱激活，后面可以加入信息激活或者电话激活之类的
    """

    def get(self, request):
        if cache.get('token') is not request.GET['u_token']:
            return HttpResponse("链接已失效")
        user = User.objects.get(userAccount=request.GET.get('u_Account'))
        user.if_activate = 1
        user.save()
        return redirect('/App/Login')


class ChangeCart(View):
    """
    通过ajax修改购物车的数据
    """

    def post(self, request, operation):
        p_id = request.POST.get("p_id")
        try:
            product = MarketGoods.objects.get(id=p_id)
        except BaseException:
            pass
        cart1 = Cart.objects.filter(
            c_user=request.user_obj).filter(
            c_goods_id=product).first()
        if cart1:
            nums = cart1.goods_nums
            if int(operation) is ADD_OPERATION:  # ADD_OPERATION代表对购物车数量做加操作
                nums = nums + 1
            if int(operation) is SUB_OPERATION:  # SUB_OPERATION代表对购物车数量做减操作
                if nums > 0:
                    nums = nums - 1
                else:
                    nums = 0
            cart1.goods_nums = nums
            cart1.save()
        else:
            cart2 = Cart()
            cart2.c_user = request.user_obj
            cart2.c_goods = product
            cart2.save()
            nums = cart2.goods_nums
        request.session['nums'] = nums
        data = {
            "status": 200,
            "msg": "成功",
            "nums": nums
        }
        return JsonResponse(data=data)


class ChangeStatus(View):
    """
    通过ajax改变商品选中的状态
    """

    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart_id = int(cart_id)
        try:
            cart1 = Cart.objects.get(pk=cart_id)
        except BaseException:
            pass
        cart1.if_selected = not cart1.if_selected
        cart1.save()
        if Cart.objects.filter(if_selected=False).exists():
            if_all_select = False
        else:
            if_all_select = True
        data = {
            'status': 200,
            'is_select': cart1.if_selected,
            'if_all_select': if_all_select,
        }
        return JsonResponse(data=data)


class ChangeAllStatus(View):
    """
    通过ajax改变购物车中所有选中的状态
    """

    def get(self, request):
        state = request.GET.get('state')
        state = int(state)
        if state is ALL_STATUS:  # 全选状态
            for i in Cart.objects.all():
                i.if_selected = False
                i.save()
        if state is NOT_ALL_STATUS:  # 不是全选状态
            for j in Cart.objects.all():
                j.if_selected = True
                j.save()
        data = {
            'status': 200
        }
        return JsonResponse(data=data)


class ChangeCartNum(View):
    """
    通过ajax修改购物车商品的数量
    """

    def get(self, request):
        pid = request.POST.get("pid")
        try:
            c_goods = MarketGoods.objects.get(pk=pid)
        except BaseException:
            pass
        cart1 = Cart.objects.filter(
            c_user=request.user_obj).filter(
            c_goods=c_goods)
        goods_nums = cart1.goods_nums
        data = {
            'goods_nums': goods_nums,
        }
        return JsonResponse(data=data)


class OrderAjax(View):
    """
    通过ajax对订单里面的商品进行排序
    """

    def get(self, request):
        user = request.user_obj
        orders = Order.objects.filter(user=user)
        data = {
            'user': request.user_obj,
            'title': '订单',
            'orders': orders,
        }
        return render(request, 'Order/Order.html/', context=data)


class AddOrder(HelperFun, View):
    """
    通过ajax添加一个订单记录，添加之后重定向到订单页面
    """

    def get(self, request):
        o = Order()
        o.user = request.user_obj
        o.o_price = super().get_total_price()
        o.save()
        for i in Cart.objects.filter(if_selected=True):
            og = OrderGoods()
            try:
                o = Order.objects.get(id=o.id)
            except BaseException:
                pass
            og.order = o
            og.market_goods = i.c_goods
            og.save()
        return redirect('/App/OrderAjax/')


def market(request):
    """ 商品展示页面

    没有分类功能的商品展示页面
    ps：在增量式开发的过程中开发的这个功能函数,已经重定向到market_with_args页面
    """
    return redirect(reverse('App:MarketWithArgs',
                            kwargs={'category_id': 104749,
                                    'child_cid': 0, 'sort_mode': 0}))


# 自定义的退出登陆函数
def out(request):
    request.session.flush()
    return redirect('/App/Mine')
