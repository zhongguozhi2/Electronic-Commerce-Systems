#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : middleware.py
# @Software: PyCharm

from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from App.models import User
from GPAXF.settings import is_ajax, no_ajax


class LoginMiddleware(MiddlewareMixin):
    """
    判断用户是否登陆的中间件
    """

    def process_request(self, request):
        # print(request.path)
        for key, value in request.META.items():
            print(key, value)
        # 如果请求的方式是ajax
        if request.path in is_ajax or request.path in no_ajax:
            if request.session.get("userAccount"):
                user_account = request.session.get("userAccount")
                try:
                    user = User.objects.get(userAccount=user_account)
                    request.user_obj = user
                except BaseException:
                    pass
            else:
                # 如果请求的方式是ajax，那么返回json数据
                if request.path in is_ajax:
                    data = {
                        "status": 600,
                        "msg": "请先登陆"
                    }
                    return JsonResponse(data=data)
                # 如果请求的方式不是ajax，那么直接重定向到登陆界面
                if request.path in no_ajax:
                    return redirect("/App/Login/")
