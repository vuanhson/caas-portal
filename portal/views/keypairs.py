from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

from .authentication import *

def keypairs(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    keypair_detail_url = 'http://'+ IP[0] + ':8774/v2.1/os-keypairs'
    keypair_detail_res = requests.get(keypair_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    if keypair_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': keypair_detail_res.json()
        }
        return render(request, 'portal/keypairs.html',context)
    return render(request, 'portal/keypairs.html')

def keypair_action(request, action, keypair_name):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})

    action_url = 'http://'+ IP[0] + ':8774/v2.1/os-keypairs/'+ keypair_name
    action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    return HttpResponseRedirect(reverse('portal:keypairs'))
