from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def networks(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    network_detail_url = 'http://'+ IP[0] + ':9696/v2.0/networks'
    network_detail_res = requests.get(network_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    subnet_detail_url = 'http://'+ IP[0] + ':9696/v2.0/subnets'
    subnet_detail_res = requests.get(subnet_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if network_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': network_detail_res.json(),
            'subnet_detail' : subnet_detail_res.json()
        }
        return render(request, 'portal/networks.html',context)
    return render(request, 'portal/networks.html')

def network_action(request, action, network_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})

    action_url = 'http://'+ IP[0] + ':9696/v2.0/networks/'+ network_id
    action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    return HttpResponseRedirect(reverse('portal:networks'))
