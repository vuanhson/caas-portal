from django import template
import requests
import time
from datetime import datetime, timedelta
from django.utils.timesince import timesince

register = template.Library()
# dung cac filter nay vi dinh ki tu dac biet (dau :) nen ko the goi truc tiep trong view
@register.filter
def instance_ipaddr_type(value):
    return value["OS-EXT-IPS:type"]

@register.filter
def instance_az(value):
    return value["OS-EXT-AZ:availability_zone"]

@register.filter
def instance_power_state(value):
    return value["OS-EXT-STS:power_state"]

@register.filter
def instance_task_state(value):
    return value["OS-EXT-STS:task_state"]

@register.filter
def network_external(value):
    return value["router:external"]

@register.filter
def ephemeral_disk(value):
    return value["OS-FLV-EXT-DATA:ephemeral"]

@register.filter
def os_flavor_access(value):
    return value["os-flavor-access:is_public"]

@register.filter
def size_convert(value):
    if 0 <= value < 1024:
        return str(value) + 'bytes'
    elif 1024 <= value < 1024**2:
        return str(round(value/1024),2) + 'KB'
    elif 1024**2 <= value < 1024**3:
        return str(round(value/(1024**2),2)) + 'MB'
    elif 1024**3 <= value < 1024**4:
        return str(round(value/(1024**3),2)) + 'GB'
    return value
#dua vao time de xac dinh khoang thoi gian tu luc tao den bay gio
@register.filter
def age(value):
    now = datetime.now()
    now = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
    value = datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%SZ")
    try:
        difference = now - value
    except:
        return value
    if difference <= timedelta(minutes=1):
        return 'Just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
