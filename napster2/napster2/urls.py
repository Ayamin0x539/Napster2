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
    url(r'^view_cart/$', views.view_cart),
    url(r'^checkout/$', views.checkout),
    url(r'^checkout/failure/$', views.checkout_failure),
    url(r'^checkout/success/$', views.checkout_success),
    url(r'^demographics/$', views.demographics),
    url(r'^addtracks/$', views.add_tracks),
    url(r'^addtracks/failure/$', views.add_tracks_failure),
    url(r'^addtracks/success/$', views.add_tracks_success),
    url(r'^addtracks/track_exists/$', views.add_tracks_exists),
#    url(r'^manageplaylist', views.manageplaylist),
    url(r'^search/$', views.search),
    url(r'^search_playlists/$', views.search_playlists),
    url(r'^view_MyPlaylist/$', views.view_MyPlaylist),
    url(r'^edit_MyPlaylist/$', views.edit_upl),
    url(r'^playlist_details/$', views.edit_epl),
    #    url(r'^checkout_success', views.checkout_success),
    url(r'^reporting/sales/$', views.sales_reporting),
    url(r'^reporting/inventory/$', views.inventory_reporting),
]
