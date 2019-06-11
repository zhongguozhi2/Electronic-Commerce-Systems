#!python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 12:59
# @Author  : 黄治文
# @File    : user_form.py
# @Software: PyCharm

from django import forms


class LoginForm(forms.Form):
    """
    登陆表单
    """
    user_name = forms.CharField(
        max_length=12,
        min_length=6,
        required=True,
        widget=forms.TextInput)
    user_password = forms.CharField(
        max_length=16,
        min_length=6,
        required=True,
        widget=forms.PasswordInput)
