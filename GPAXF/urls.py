"""GPAXF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.HomeVIew, name='HomeVIew')
Class-based views
    1. Add an import:  from other_app.views import HomeVIew
    2. Add a URL to urlpatterns:  url(r'^$', HomeVIew.as_view(), name='HomeVIew')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^App/', include('App.urls', namespace='App'))

]
