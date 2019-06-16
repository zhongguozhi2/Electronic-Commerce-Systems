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
from django.views.generic import View, ListView, DetailView, RedirectView, CreateView, FormView, UpdateView

from App.form.user_form import RegisterForm
from App.views_helper import HelperMixin
from GPAXF import settings
from GPAXF.settings import COMPREHENSIVE_ORDER, SALES_QUANTITY_ORDER, PRICE_ASE_ORDER, \
    PRICE_DESC_ORDER, ADD_OPERATION, SUB_OPERATION, NOT_ALL_STATUS, ALL_STATUS
from .models import *
# Create your views here.


# 方法装饰器，指定装饰dispatch方法，可以应用到类，因为不管是什么类型的请求，都会走先走dispatch方法
@method_decorator(cache_page(60), name='dispatch')
class HomeView(ListView):
    """主页

    展示项目的主要信息，包括：轮播展示部分热卖商品，商品导航栏，必买商品和超市
    """
    model = AxfHomeMainShow
    template_name = 'main/Home.html'
    extra_context = {'title': '主页'}

    def get_queryset(self):
        self.wheel_datas = AxfHomeWheels.objects.all()
        self.nav_datas = AxfHomeNav.objects.all()
        self.must_buy_datas = AxfHomeMustBuy.objects.all()
        self.shop_datas = AxfShop.objects.all()
        self.shop0_1_datas = self.shop_datas[0:1]  # 取出闪送超市对象
        self.shop1_3_datas = self.shop_datas[1:3]  # 取出热卖商品对象
        self.shop3_7_datas = self.shop_datas[3:7]  # 取出分类商品对象
        self.shop7_11_datas = self.shop_datas[7:11]  # 取出超市商品对象
        return super(HomeView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['nav_datas'] = self.nav_datas
        context['wheel_datas'] = self.wheel_datas
        context['must_buy_datas'] = self.must_buy_datas
        context['shop0_1_datas'] = self.shop0_1_datas
        context['shop1_3_datas'] = self.shop1_3_datas
        context['shop3_7_datas'] = self.shop3_7_datas
        context['shop7_11_datas'] = self.shop7_11_datas
        return context

# 方法装饰器，指定装饰dispatch方法，可以应用到类，因为不管是什么类型的请求，都会走先走dispatch方法
@method_decorator(cache_page(60), name='dispatch')
class MarketWithArgsView(ListView):
    """商品展示页面

    展示项目的全部商品，根据不同的类别展示不同的商品，用户可以选择不同的排序方式，包括：综合排序
    销量排序，价钱高低排序等
    """
    model = MarketGoods
    template_name = 'main/market.html'
    extra_context = {'title': '闪购'}

    def get_queryset(self):
        goods_type_datas = super(MarketWithArgsView, self).get_queryset()
        return goods_type_datas.filter(category_id=self.kwargs['category_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MarketWithArgsView, self).get_context_data()
        category_id = int(self.kwargs['category_id'])
        child_cid = int(self.kwargs['child_cid'])
        sort_mode = int(self.kwargs['sort_mode'])
        type_datas = GoodsType.objects.all()
        child_category_datas = [j for j in [i.split(':')  # 列表生成式方法取出子类的数据
                                            for i in GoodsType.objects.filter
                                            (typeid=category_id)[0].childtypenames.split('#')]]
        goods_by_cid_datas = self.get_queryset().filter(child_cid=child_cid)
        if child_cid is COMPREHENSIVE_ORDER:  # 综合排序
            goods_datas = self.get_queryset()
        else:
            goods_datas = goods_by_cid_datas
        if sort_mode is SALES_QUANTITY_ORDER:  # 按销售数量排序
            goods_datas = goods_datas.order_by("product_num")
        if sort_mode is PRICE_ASE_ORDER:  # 按价格升序排序
            goods_datas = goods_datas.order_by("price")
        if sort_mode is PRICE_DESC_ORDER:  # 按价格降序排序
            goods_datas = goods_datas.order_by("-price")
        context = context.update({
            'category_id': category_id,
            'child_cid': child_cid,
            'type_datas': type_datas,
            'goods_type_datas': self.get_queryset(),
            'child_category_datas': child_category_datas,
            'goods_datas': goods_datas,
            'sort_mode': sort_mode,
        })
        return context


# 登陆界面
class Login(LoginView):
    template_name = 'user/Login.html'

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """注册账号页面

    用户可以在这个页面注册账号
    ps：后端已完成，前端开发一部分，后面打算用vue来完善
    """
    template_name = 'user/Register.html'
    success_url = '/App/MineView/'
    model = User
    fields = ['user_account', 'user_password', 'user_address',
              'user_phone', 'user_name', 'user_icon', 'user_rank',
              'user_token', 'if_activate', ]

    def form_valid(self, form):
        # 更改默认ModelForm的user_password值，使用hash摘要算法加密注册密码，防止内部人员看到密码
        super(
            RegisterView,
            self).kwargs['user_password'] = hashlib.md5(
            (super(
                RegisterView,
                self).kwargs['user_password'] +
                'salt').encode('utf-8')).hexdigest()
        self.storage_path()
        self.send_email()
        return super(RegisterView, self).form_valid(form)

    def storage_path(self):
        """
        存储头像
        :return:
        """
        storage_path = os.path.join(settings.MDEIA_ROOT, super(
            RegisterView, self).kwargs['user_account'] + '.png')
        with open(storage_path, "wb") as fp:
            for i in super(RegisterView, self).kwargs['user_icon'].chunks():
                fp.write(i)

    def send_email(self):
        """
        发送email，用于激活账户
        :return:
        """
        token = uuid.uuid4().hex  # uuid生成一个永不相等的随机字符串
        cache.set('token', token, 24 * 60 * 60)
        activate_template = loader.get_template('user/email.html'). render(
            {'user_account': super(RegisterView, self).kwargs['user_account'], 'token': token})
        # 发送邮件激活账号，这里用的是网易邮箱，后面可分离出来，加入其他激活方式
        send_mail(
            subject='Activate axf',
            message='hello',
            from_email='xiaozhizhi_0@163.com',
            recipient_list=[
                'xiaozhizhi_0@163.com',
            ],
            html_message=activate_template)


class QuitView(RedirectView):
    """
    退出登陆,之后重定向到个人中心界面
    """
    url = '/App/Mine/'
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(QuitView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(QuitView, self).get(request, *args, **kwargs)


class CheckUserIdView(View):
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


class MineView(DetailView):
    """ 用户的个人中心展示界面

    展示用户的信息，目前只展示了用户的用户名、头像等基本信息，后面添加更多有用的信息
    """
    model = User
    template_name = 'main/Mine.html'
    extra_context = {'title': '我的'}

    def get(self, request, *args, **kwargs):
        try:
            request_token = request.session.get('tok')  # 验证token
            user = User.objecs.get(userToken=request_token)
        except User.DoesNotExist:
            return redirect("/App/Login/")
        else:
            self.user_name = user.user_name
        return super(MineView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['username'] = self.user_name
        return context


class CartView(HelperMixin, ListView):
    """购物车页面

    这个页面展示用户在market_with_args页面添加的商品，显示的主要有用户的信
    息、地址、购物车商品，用户在这个页面
    还可以增加和删除购物的商品，和一个添加为订单的按钮，生成订单
    """
    model = Cart
    template_name = 'main/Cart.html'
    context_object_name = 'carts'
    extra_context = {'title': '购物车'}

    def get_queryset(self):
        carts = super(CartView, self).get_queryset()
        if carts.filter(if_selected=False).exists():
            self.if_all_select = False
        else:
            self.if_all_select = True
        self.total_price = super(CartView, self).get_total_price()
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['total_price'] = self.total_price
        context['if_all_select'] = self.if_all_select
        return context


class ActivateView(RedirectView):
    """激活账号

    通过发送邮箱的方式激活已经注册好的账号
    ps：目前提供的是网易邮箱激活，后面可以加入信息激活或者电话激活之类的
    """
    pattern_name = 'Login'

    def get(self, request, *args, **kwargs):
        if cache.get('token') is not request.GET['u_token']:
            return HttpResponse("链接已失效")
        user = User.objects.get(userAccount=request.GET.get('u_Account'))
        user.if_activate = 1
        user.save()
        return super(ActivateView, self).get(self, request, *args, **kwargs)


class AjaxResponseMixin:
    """
    对于一个表单，增加一个Ajax支持
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class ChangeCartView(AjaxResponseMixin, UpdateView):
    """
    通过ajax修改购物车的数据
    """
    model = Cart
    fields = ['goods_nums', 'c_user', 'c_goods']

    def get_object(self, queryset=None):
        object_with_filter = super(ChangeCartView, self).get_object()
        p_id = self.request.POST.get("p_id")
        try:
            product = MarketGoods.objects.get(id=p_id)
        except BaseException:
            pass
        object_with_filter = object_with_filter.filter(
            c_user=self.request.user_obj).filter(
            c_goods_id=product).first()
        return object_with_filter

    def form_valid(self, form):

        if self.object.exists():
            nums = self.object.goods_nums
            if int(self.kwargs['operation']
                   ) is ADD_OPERATION:  # ADD_OPERATION代表对购物车数量做加操作
                nums = nums + 1
            if int(self.kwargs['operation']
                   ) is SUB_OPERATION:  # SUB_OPERATION代表对购物车数量做减操作
                if nums > 0:
                    nums = nums - 1
                else:
                    nums = 0
            form.instance.goods_nums = nums
        else:
            form.instance.c_user = self.request.user_obj
            form.instance.c_goods = self.request.product
            nums = self.object.goods_nums
        self.request.session['nums'] = nums
        return super(ChangeCartView, self).form_valid(form)


class ChangeStatusView(AjaxResponseMixin, UpdateView):
    """
    通过ajax改变商品选中的状态
    """
    model = Cart
    fields = ['if_selected']

    def form_valid(self, form):
        form.instance.if_selected = not self.object.if_selected
        if self.object.filter(if_selected=False).exists():
            if_all_select = False
        else:
            if_all_select = True
        # 重新给AjaxResponseMixin中的data赋值
        data = {
            'status': 200,
            'is_select': self.object.if_selected,
            'if_all_select': if_all_select,
        }
        return super(ChangeStatusView, self).form_valid(form)


class ChangeAllStatusView(AjaxResponseMixin, UpdateView):
    """
    通过ajax改变购物车中所有选中的状态
    """
    model = Cart
    fields = ['if_selected']
    def form_valid(self, form):

        state = self.kwargs.get('state')
        state = int(state)
        if state is ALL_STATUS:  # 全选状态
            for i in Cart.objects.all():
                i.if_selected = False
        if state is NOT_ALL_STATUS:  # 不是全选状态
            for j in Cart.objects.all():
                j.if_selected = True
        data = {
            'status': 200
        }
        return super(ChangeAllStatusView, self).form_valid(form)


class ChangeCartNumView(View):
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


class AddOrderView(HelperMixin, RedirectView, UpdateView):
    """
    通过ajax添加一个订单记录，添加之后重定向到订单页面
    """
    model = Order
    pattern_name = 'OrderAjax'
    fields = ['order', 'user', 'o_price', 'market_goods']

    def form_valid(self, form):
        form.instance.user = self.request.user_obj
        form.instance.o_price = super().get_total_price()
        for i in Cart.objects.filter(if_selected=True):
            order_goods = OrderGoods()
            try:
                order_obj = Order.objects.get(id=self.pk_url_kwarg)
            except BaseException:
                pass
            form.instance.order = order_obj
            form.instance.market_goods = i.c_goods

        return super(AddOrderView, self).form_valid(form)


class OrderAjaxView(View):
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
