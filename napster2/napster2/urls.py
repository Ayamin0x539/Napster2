"""napster2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from napster2 import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^register/success/$', views.register_success),
    url(r'^login/$', 'django.contrib.auth.views.login'), 
    url(r'^dashboard/$', views.dashboard),
    url(r'^manage/$', views.update_account_info),
    url(r'^update/success/$', views.update_success),
    url(r'^logout/$', views.logout_page),
#    url(r'^manageplaylist', views.manageplaylist),
#    url(r'^search', views.search),
]
