"""g_match_ms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from match_ms.views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'match', UsersMatchList)
router.register(r'accepted', UserAcceptedList)
router.register(r'rejected', UserRejectedList)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^emparejamiento/$', match),
    url(r'^emparejamiento/usuario/(?P<pk>[0-9]+)$', listMatchUser),
    url(r'^emparejamiento/rechazados', listUsersRejected),
    url(r'^emparejamiento/rechazados/usuario/(?P<pk>[0-9]+)$', listUserRejectedByUser),
    url(r'^emparejamiento/aceptados$', listUsersAccepted),
    url(r'^emparejamiento/aceptados/usuario/(?P<pk>[0-9]+)$', listUserAcceptedByUser),
    url(r'^emparejamiento/posibles$', possibleMatch),
    url(r'^emparejamiento/filtrar-gustos', filterUserPleasures.as_view(), name='filter_user_pleasures'),


]
